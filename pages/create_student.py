#!/usr/bin/python3
from io import BytesIO, StringIO
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import getClassrooms, getClassroom, getStudentById, getStudentsIdandNames, getclassSubjects
from models.portal.admission import Admission
from models.portal.Class import Class
from models.portal.department import Department

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User

st.set_page_config(
    page_title="Create Student",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an app to manage student result"
    }
)
st.title("Add Students")

def create_student():
    st.header("Add Students")
    st.info("Please ensure not two students with the same full name are the same arm")
    st.info("Please enter the form manually dont autofill")
    code = st.selectbox("Class", getClassrooms())
    if code:
        clss =  getClassroom(code)
    firstName = st.text_input("First Name", placeholder="First Name")
    middleName = st.text_input("Middle Name", placeholder="Middle Name")
    lastName = st.text_input("Last Name", placeholder="last Name")
    admission_Number = st.text_input("Admission Number", placeholder="Admission Number")
    gender = st.selectbox("Gender", ["Male", "Female"])
    if st.button("Add student") and firstName and lastName and admission_Number and clss:

        stud = Student()
        stud.firstName = firstName.upper()
        stud.middleName = middleName.upper()
        stud.lastName = lastName.upper()
        stud.admission_no = admission_Number.upper()
        stud.gender = gender
        stud.classroom_id = clss.id
        stu = Admission.query.filter(Admission.admission_no==stud.admission_no).one_or_none()
        if stu:
            st.error(f"{stu.fullName} has {admission_Number} as admission number")
            return
        stud.save()
        st.success(f"{stud.fullName} created successfuly with id: {stud.id}")

create_student()