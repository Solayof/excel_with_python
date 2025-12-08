#!/usr/bin/python3
import datetime
from io import BytesIO, StringIO
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import getClassrooms, getClassroom, getStudentById, getStudentsIdandNames, getclassSubjects, departs_name_with_id
from models.portal.teacher import Teacher
from models.portal.department import Department
from models.portal.user import User
from pages import session_auth

current_user = session_auth.current_user()
if not current_user:
    st.switch_page("CHS_IGBOPE_PORTAL.py")
if current_user.isAdmin() is False:
    st.switch_page("CHS_IGBOPE_PORTAL.py")

st.set_page_config(
    page_title="Create Teacher",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an app to manage student result"
    }
)
st.title("Create Teacher")
def create_teacher():
    departs_dict = departs_name_with_id()
    st.header("Add Teacher")
    name = st.selectbox("Department", departs_dict.keys())
    username = st.text_input("Username", placeholder="Username")
    depart_id = departs_dict.get(name, None) if name else None
    firstName = st.text_input("First Name", placeholder="First Name")
    middleName = st.text_input("Middle Name", placeholder="Middle Name")
    lastName = st.text_input("Last Name", placeholder="last Name")
    email = st.text_input("Email", placeholder="Email")
    phone = st.text_input("Phone Number", placeholder="Phone Number")
    gender = st.selectbox("Gender", ["Male", "Female"])
    dob = st.date_input(
    "Date of Birth",
    value=datetime.date(2000, 1, 1),   # default selected date
    min_value=datetime.date(1900, 1, 1),  # earliest date allowed
    max_value=datetime.date.today()       # latest date allowed
    )
    password = st.text_input("Password", placeholder="Password", type="password")
    confirm_password = st.text_input("Confirm Password", placeholder="Confirm Password", type="password")
    address = st.text_input("Address", placeholder="Address")
    staff_id = st.text_input("Staff ID", placeholder="Staff ID")
    file_no = st.text_input("File Number", placeholder="File Number")
    grade_level = st.text_input("Grade Level", placeholder="Grade Level")
    previous_school = st.text_input("Previous School", placeholder="Previous School")
    date_transfer = st.date_input("Date of Transfer", max_value=datetime.date.today())
    last_promotion_date = st.date_input("Last Promotion Date", max_value=datetime.date.today())
    
    if st.button("Add Teacher") and username and firstName and lastName and password and depart_id:
        if User.query.filter_by(email=email).one_or_none():
            st.error(f"User with the email exists")
            return
        if User.query.filter_by(username=username).one_or_none():
            st.error(f"User with the username exists")
            return
        if password != confirm_password:
            st.error("Password and confirm password not the same")
            return
        teacher = Teacher()
        teacher.username = username
        teacher.password = password
        teacher.firstName = firstName.upper()
        teacher.middleName = middleName.upper()
        teacher.last_promote_date = last_promotion_date
        teacher.lastName = lastName.upper()
        teacher.gender = gender
        teacher.grade_level = grade_level
        if Teacher.query.filter_by(file_no=file_no).one_or_none():
            st.error("Teacher with the file number exists")
            return
        teacher.file_no = file_no
        teacher.previous_school = previous_school
        teacher.date_transfer = date_transfer
        if Teacher.query.filter_by(staff_id=staff_id).one_or_none():
            st.error("Teacher with the staff id exists")
            return
        teacher.staff_id = staff_id
        teacher.dob = dob
        teacher.phone_number = phone
        teacher.department_id = depart_id
        teacher.address = address
        teacher.email = email
        teacher.save()
        st.success(f"{teacher.fullName} created successfuly with id: {teacher.id}")

create_teacher()