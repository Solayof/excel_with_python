#!/usr/bin/python3
import datetime
from io import BytesIO, StringIO
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import getClassrooms, getClassroom, getStudentById, getStudentsIdandNames, getclassSubjects, departs_name_with_id
from models.portal.admission import Admission
from models.portal.Class import Class
from models.portal.department import Department

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User
from pages import session_auth

current_user = session_auth.current_user()
if not current_user:
    st.switch_page("CHS_IGBOPE_PORTAL.py")
if current_user.isAdmin() is False:
    st.switch_page("CHS_IGBOPE_PORTAL.py")

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
    username = st.text_input("Username", placeholder="Username")
    firstName = st.text_input("First Name", placeholder="First Name")
    middleName = st.text_input("Middle Name", placeholder="Middle Name")
    lastName = st.text_input("Last Name", placeholder="last Name")
    admission_Number = st.text_input("Admission Number", placeholder="Admission Number")
    gender = st.selectbox("Gender", ["Male", "Female"])
    email = st.text_input("Email", placeholder="Email")
    phone = st.text_input("Phone Number", placeholder="Phone Number")
    dob = st.date_input(
    "Date of Birth",
    value=datetime.date(2000, 1, 1),   # default selected date
    min_value=datetime.date(2000, 1, 1),  # earliest date allowed
    max_value=datetime.date.today()       # latest date allowed
    )
    password = st.text_input("Password", placeholder="Password", type="password")
    confirm_password = st.text_input("Confirm Password", placeholder="Confirm Password", type="password")
    address = st.text_input("Address", placeholder="Address")
    
    if st.button("Add student") and firstName and lastName and admission_Number and clss:
        user = User.query.filter_by(email=email).one_or_none()
        if User.query.filter_by(email=email).one_or_none():
            st.table(pd.DataFrame([user.to_dict()]), use_container_width=True)
            st.error(f"User with the email exists")
            return
        if User.query.filter_by(username=username).one_or_none():
            user = User.query.filter_by(username=username).one_or_none()
            st.table(pd.DataFrame([user.to_dict()]), use_container_width=True)
            st.error(f"User with the username exists")
            return
        if password != confirm_password:
            st.error("Password and confirm password not the same")
            return
        stud = Student()
        stud.username = username
        stud.firstName = firstName.upper()
        stud.middleName = middleName.upper()
        stud.lastName = lastName.upper()
        stud.admission_no = admission_Number.upper()
        stud.gender = gender
        stud.classroom_id = clss.id
        stud.password = password
        stud.address = address
        stud.dob = dob
        stud.email = email
        stud.phone_number = phone
        stu = Admission.query.filter(Admission.admission_no==stud.admission_no).one_or_none()
        if stu:
            st.error(f"{stu.fullName} has {admission_Number} as admission number")
            return
        stud.save()
        st.success(f"{stud.fullName} created successfuly with id: {stud.id}")

create_student()