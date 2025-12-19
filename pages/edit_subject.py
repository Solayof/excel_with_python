#!/usr/bin/python3
from datetime import datetime
from io import BytesIO, StringIO
import logging
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import (get_classroom_id, getClassrooms, getclassSubjects,
                          students_with_subject_dict)
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
st.title("Edit Student Subject Score")

def edit_subject():
    st.header("Update Scores")
    stud = None
    term = None
    code = st.selectbox("Class", getClassrooms())
    subjectlist = getclassSubjects(code)
    subjectname = st.selectbox("Subject", subjectlist)
    term_lists = term_list()
    term = st.selectbox("Term", term_lists, index=term_lists.index(current_term()))
    fullNameId = students_with_subject_dict(
        subject_name=subjectname,
        term=term,
        session=current_session(),
        classroom_id=get_classroom_id(code)
    )
    name = st.selectbox("Name", fullNameId.keys())
    if name:
        stud = Student.query.filter_by(id=fullNameId[name]).one_or_none()
        subject = Subject.query.filter_by(
            student_id=stud.id, name=subjectname, session=current_session(), term=term).one_or_none()
        if subject:
            ca = st.number_input("Continuous Assessment", 0, 30, subject.CA)    
            exam = st.number_input("Examination Score", 0, 70, subject.examScore)

            if st.button("Update"):
                subject.CA = ca
                subject.examScore = exam
                subject.save()
                logger.info(f"Subject score for {subjectname} updated for {name} in {term} {current_session()} academic session by {current_user.fullName}")

                st.success("score updated successfully")
try:
    edit_subject()
except Exception as e:
    logger.error(f"Error in editing subject score: {e}")
    st.error("An error occurred while editing the subject score.")