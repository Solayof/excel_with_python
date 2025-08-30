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
st.title("Delete Student Subject Score")

def delete_subject():
    st.header("Delete Scores")
    code = st.selectbox("Class", getClassrooms())
    subjectname = None
    name = None
    stud = None
    if code:
        fullNameId = getStudentsIdandNames(code)
        name = st.selectbox("Name", fullNameId.keys())
        if name:
            stud = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
            term_lists = term_list()
        term = st.selectbox("Term", term_lists, index=term_lists.index(current_term()))
        if stud and term:
            subjectlist = [sub for sub in getclassSubjects(code) if sub in stud.subject_recorded(term=term)]
            subjectname = st.selectbox("Subject", subjectlist)
            sessions = session_list()
            if current_session() not in sessions:
                sessions.append(current_session())
            session = st.selectbox("Session", sessions, index=sessions.index(current_session()))
    
            subject = Subject.query.filter_by(
                student_id=stud.id, name=subjectname, session=session).one_or_none()
            if subject:
                st.write(f"CA: {subject.CA}, Exam Score: {subject.examScore}, Total Score: {subject.totalScore}")
                if st.button("Delete"):
                    subject.delete()
                    st.success("Subject score deleted successfully")

delete_subject()