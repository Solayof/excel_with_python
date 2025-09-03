#!/usr/bin/python3
from datetime import datetime
from io import BytesIO, StringIO
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

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User

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


def report_sheet():
    st.header("Report Sheet")
    code = st.selectbox("Class", getClassrooms())

    if code:
        fullNameId = getStudentsIdandNames(code)
        name = st.selectbox("Name", fullNameId.keys())
        term_lists = term_list()
        term = st.selectbox("Term", term_lists, index=term_lists.index(current_term()))
        sessions = session_list()
        current_sess = current_session()
        if current_sess not in sessions:
            sessions.append(current_sess)
        session = st.selectbox("Session", sessions, index=sessions.index(current_sess))
        if name:
            stud = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
        if stud:
            subs_list = []
            subjectlist = [sub for sub in getclassSubjects(code) if sub in stud.subject_recorded(term=term, session=session)]
            for sub in subjectlist:
                obj = {}
                obj["SUBJECT"] = sub
                sub_dict = stud.records_for_subject(subject=sub, term=term, session=session)
                obj.update(sub_dict)
                obj["TOTAL"] = sum(sub_dict.values())
                subs_list.append(obj)
                df = pd.DataFrame(subs_list)
            st.dataframe(df.sort_values(by="TOTAL", ascending=False))

report_sheet()