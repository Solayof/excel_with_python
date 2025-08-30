#!/usr/bin/python3
from io import BytesIO, StringIO
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import getClassrooms, getClassroom, getStudentById, getStudentsIdandNames, getclassSubjects
from models.portal.admission import Admission
from models.portal.Class import Class

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
st.title("Edit Students")

def edit_student():
    code = st.selectbox("Class", getClassrooms())

    if code:
        fullNameId = getStudentsIdandNames(code)
        name = st.selectbox("Name", fullNameId.keys())

    if name:
        stud = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
        if stud:
            firstName = st.text_input("First Name", placeholder="First Name", value=stud.firstName)
            middleName = st.text_input("Middle Name", placeholder="Middle Name", value=stud.middleName)
            lastName = st.text_input("Last Name", placeholder="last Name", value=stud.lastName)
            admission_Number = st.text_input("Admission Number", placeholder="Admission Number", value=stud.admission_no)
            gender = st.selectbox("Gender", ["Male", "Female"])

        if st.button("Update student") and stud:
            stud.firstName = firstName.upper()
            stud.middleName = middleName.upper()
            stud.lastName = lastName.upper()
            stud.admission_no = admission_Number.upper()
            stud.gender = gender

            stud.save()
            st.dataframe(pd.DataFrame([stud.to_dict()]))
            st.success("Updated successfuly")

edit_student()