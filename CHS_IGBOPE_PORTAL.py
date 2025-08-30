#!/usr/bin/python3
from io import BytesIO, StringIO
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from models import storage


from models.portal.admission import Admission
from models.portal.Class import Class

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User


if __name__ == "__main__":
    storage.create_table()
@st.cache_data(ttl=5000)
def getClassrooms():
    return Class.all()

@st.cache_data(ttl=5000)
def getStudentsIdandNames(code):
    clss = Class.query.filter_by(code=code).one_or_none()
    return clss.getStudentsIdandNames()

@st.cache_data(ttl=5000)
def getclassSubjects(code):
     clss = Class.query.filter_by(code=code).one_or_none()
     return clss.sheetSubjects

@st.cache_data(ttl=60000)
def getClassroom(code):
    return Class.query.filter_by(code=code).one_or_none()

@st.cache_data(ttl=30000)
def getStudentById(id):
    return Student.query.filter_by(id=id).one_or_none()

def viewStream():
    st.set_page_config(
        page_title="CHS BROADSHEET",
        layout="wide"
    )
    st.title("COMPREHENSIVE HIGH SCHOOL IGBOPE")
    st.title("Broadsheet Database")
    create_stud, create_sub, create_cls, change_cls, edit_stud, edit_sub, view_stud, delete_stud, delete_sub=st.columns(9)
    if create_cls.button("Add class"):
        st.switch_page("pages/create_class.py")
    if create_stud.button("Add student"):
        st.switch_page("pages/create_student.py")
    if edit_stud.button("Edit Student"):
        st.switch_page("pages/edit_student.py")
    if change_cls.button("Change Student Class"):
        st.switch_page("pages/change_class.py")
    if create_sub.button("Upload score"):
        st.switch_page("pages/create_subject")
    if edit_sub.button("Update score"):
        st.switch_page("pages/edit_subject.py")
    if view_stud.button("View student scores"):
        st.switch_page("pages/view_student_score.py")
    if delete_sub.button("Delete Students Score"):
        st.switch_page("pages/delete_subject.py")
    if delete_stud.button("Delete sudent"):
        st.switch_page("pages/delete_student.py")


viewStream()