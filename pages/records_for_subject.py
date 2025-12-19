#!/usr/bin/python3
from datetime import datetime
from io import BytesIO, StringIO
import logging
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import (getClassrooms,
                          getClassroom,
                          getStudentById,
                          getStudentsIdandNames,
                          getclassSubjects,
                          session_list)
from models.portal.admission import Admission
from models.portal.cache import current_session, current_term, term_list
from models.portal.Class import Class
from models.portal.department import Department

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User
from pages import session_auth

logger = logging.getLogger(__name__)

current_user = session_auth.current_user()
if not current_user:
    st.switch_page("CHS_IGBOPE_PORTAL.py")
if current_user.isAdmin() is False:
    st.switch_page("CHS_IGBOPE_PORTAL.py")


st.set_page_config(
    page_title="Record Student Subject Score",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an app to manage student result"
    }
)
st.title("View Student Subject Score")


def record_for_subject():
    st.header("Subject Recorded")
    code = st.selectbox("Class", getClassrooms())
    subject = None
    students = []
    subjectlist = []
    if code:
        clss =  getClassroom(code)
        if clss:
            students = Student.query.filter_by(classroom_id=clss.id).all()
            subjectlist = [sub for sub in getclassSubjects(code)]
        term_lists = term_list()
        term = st.selectbox("Term", term_lists, index=term_lists.index(current_term()))
        sessions = session_list()
        current_sess = current_session()
        if current_sess not in sessions:
            sessions.append(current_sess)
        session = st.selectbox("Session", sessions, index=sessions.index(current_sess))
        subjectname = st.selectbox("Subject", subjectlist)
        studentlist = []
        for stud in students:
            obj = {}
            obj["FULLNAME"] = stud.fullName
            sub_dict = stud.records_for_subject(subject=subjectname, term=term, session=session)
            obj.update(sub_dict)
            obj["TOTAL"] = sum(sub_dict.values())

            studentlist.append(obj)

        if studentlist:
            stdf = pd.DataFrame(studentlist)
            st.dataframe(stdf.sort_values(by="TOTAL", ascending=False))
            pldf = stdf[["FULLNAME", "TOTAL"]]
            fig = px.bar(pldf, x="FULLNAME", y="TOTAL", 
                title=f"Class {code} {subjectname}- Average Performance",
                labels={"TOTAL": "Total Score"}, 
                color="TOTAL", height=500)
            st.plotly_chart(fig, width='content')

try:
    record_for_subject()
except Exception as e:
    logger.error(f"Error in viewing records for subject: {e}")
    st.error("An error occurred while viewing the records for the subject.")