#!/usr/bin/python3
import streamlit as st



from models.portal.admission import Admission
from models.portal.Class import Class

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User

@st.cache_data(ttl=5000)
def getClassrooms():
    return Class.all()

@st.cache_data(ttl=5000)
def getStudentsIdandNames(code):
    clss = Class.query.filter_by(code=code).one_or_none()
    if clss:
        return clss.getStudentsIdandNames()

@st.cache_data(ttl=5000)
def getclassSubjects(code):
     clss = Class.query.filter_by(code=code).one_or_none()
     if clss:
        return clss.sheetSubjects

@st.cache_data(ttl=60000)
def getClassroom(code):
    return Class.query.filter_by(code=code).one_or_none()

@st.cache_data(ttl=30000)
def getStudentById(id):
    return Student.query.filter_by(id=id).one_or_none()

@st.cache_data(ttl=30000)
def session_list():
    subjects = Subject.query.with_entities(Subject.session).distinct().all()
    return [sub[0] for sub in subjects if sub[0]]

st.cache_data(ttl=30000)
def grade(score):
                    if score >= 70: return "A"
                    elif score >= 60: return "B"
                    elif score >= 50: return "C"
                    elif score >= 40: return "D"
                    else: return "F"