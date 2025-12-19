#!/usr/bin/python3
from datetime import datetime
from io import BytesIO, StringIO
import logging
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import (departs_name_with_id, getClassrooms,
                          get_classroom_id,
                          getStudentById,
                          getStudentsIdandNames,
                          getclassSubjects,
                          session_list,
                          students_without_subject_dict)
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
st.title("Record Student Subject Score")
def create_subject():
    st.header("Upload Scores")

    code = st.selectbox("Class", getClassrooms())
    subjectlist = getclassSubjects(code)
    subjectname = st.selectbox("Subject", subjectlist)
    term_lists = term_list()
    term = st.selectbox("Term", term_lists, index=term_lists.index(current_term()))
    fullNameId = students_without_subject_dict(
        subject_name=subjectname,
        term=term,
        session=current_session(),
        classroom_id=get_classroom_id(code)
    )
    name = st.selectbox("Name", fullNameId.keys())
    if name:
        student = Student.query.filter_by(id=fullNameId[name]).one_or_none()
    ca = st.number_input("Continuous Assessment", 0, 30)
    exam = st.number_input("Examination Score", 0, 70)

    if st.button("upload score") and name and subjectname and ca and exam and student:
        mth = datetime.now().strftime("%m")
        if term == "First Term" and mth not in ['09', '10', '11', '12']:
            st.warning("You are recording first term score outside first term period")
            return
        if term == "Second Term" and mth not in ['01', '02', '03', '04']:
            st.warning("You are recording second term score outside second term period")
            return
        if term == "Third Term" and mth not in ['05', '06', '07', '08']:
            st.warning("You are recording third term score outside third term period")
            return
        sub  = Subject.query.filter_by(
                    name=subjectname,
                    student_id=student.id,
                    term=term,
                    session=current_session()
                    ).one_or_none()
        if sub:
            st.error(f"Score for {subjectname} already recorded for {name} in {term} {current_session()} academic session")
            return
        subject = Subject()
        subject.name = subjectname
        subject.student_id = student.id
        subject.CA = ca
        subject.examScore = exam
        subject.term = term
        subject.session = current_session()
        if not subject.student_id:
            st.error("score can not be save, no student attached")
        subject.save()
        logger.info(f"Score for {subjectname} recorded for {name} in {term} {current_session()} academic session by {current_user.fullName}")
        st.success("score save successfully")
try:
    create_subject()
except Exception as e:
    st.error(f"An error occurred: {e}")
    logger.error(f"Error in creating subject score: {e}")