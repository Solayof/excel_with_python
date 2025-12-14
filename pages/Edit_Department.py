#!/usr/bin/python3
import datetime
from io import BytesIO, StringIO
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy.orm.attributes import flag_modified
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
    page_title="Update Department",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an app to manage student result"
    }
)
st.title("Create Department")

def update_department_subject():
    all_subjects = (
        "General Mathematics", "English Language", "Basic Science", "Basic Technology",
        "Social Studies", "Civic Education",
        "C.R.S", "IRS", "Islamic Studies", "Business Studies",
        "P.H.E", "Agricultural Science",
        "Imformation Technology", "Yoruba",
        " Livestock farming,", "English Language", "Biology", "Chemistry", "Physics",
        "Geography", "Economics",
        "CRS", "Government", "Literature in English",
        "Commerce", "Financial Accounting"
    )
    depart_dict = departs_name_with_id()
    name = st.selectbox("Department Name", depart_dict.keys())
    if name:
        depart = Department.query.filter_by(name=name.upper()).one_or_none()
        selected_subjects = st.multiselect("Select your subjects:", all_subjects, depart.subjects)
        if st.button("Update Department") and name and selected_subjects:
            depart.subjects = selected_subjects
            flag_modified(depart, "subjects")
            depart.save()
            st.success(f"Department {name} updated successfully")
            st.dataframe(pd.DataFrame([depart.to_dict()]))
 
update_department_subject()