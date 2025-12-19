#!/usr/bin/python3
import datetime
from io import BytesIO, StringIO
import logging
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import getClassrooms, getClassroom, getStudentById, getStudentsIdandNames, getclassSubjects, departs_name_with_id
from models.portal.teacher import Teacher
from models.portal.department import Department
from models.portal.user import User
from pages import session_auth

logger = logging.getLogger(__name__)

current_user = session_auth.current_user()
if not current_user:
    st.switch_page("CHS_IGBOPE_PORTAL.py")
if current_user.isAdmin() is False:
    st.switch_page("CHS_IGBOPE_PORTAL.py")

st.set_page_config(
    page_title="Create Department",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an app to manage student result"
    }
)
st.title("Create Department")

def create_department():
    all_subjects = (
        "General Mathematics", "English Language", "Basic Science", "Basic Technology",
        "Social Studies", "Civic Education",
        "C.R.S", "Islamic Studies", "Business Studies",
        "P.H.E", "Agricultural Science",
        "Imformation Technology", "Yoruba",
        " Livestock farming,", "English Language", "Biology", "Chemistry", "Physics",
        "Geography", "Economics",
        "CRS", "Government", "Literature in English",
        "Commerce", "Financial Accounting"
    )
    name = st.text_input("Department Name", placeholder="Department Name")
    selected_subjects = st.multiselect("Select your subjects:", all_subjects)
    if st.button("Add Department") and name and selected_subjects:
        depart = Department(name=name.upper())
        selected_subjects = [sub.upper() for sub in selected_subjects]
        depart.subjects = selected_subjects
        if Department.query.filter_by(name=name.upper()).one_or_none():
            st.warning(f"Department {name} exists")
            return
        depart.save()
        logger.info(f"Department {name} created by {current_user.fullName}")
        st.success(f"Department {name} created successfully")
        st.dataframe(pd.DataFrame([depart.to_dict()]))

try:
    create_department()
except Exception as e:
    logger.error(f"Error in creating department: {e}")
    st.error("An error occurred while creating the department.")
