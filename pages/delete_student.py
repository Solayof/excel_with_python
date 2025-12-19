#!/usr/bin/python3
from io import BytesIO, StringIO
import logging
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
from pages import session_auth

logger = logging.getLogger(__name__)
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
st.title("Delete Students")


def delete_student():
    code = st.selectbox("Class", getClassrooms())
    name = None
    student = None
    if code:
        fullNameId = getStudentsIdandNames(code)
        if fullNameId:
            st.info("Select a student to delete")
            name = st.selectbox("Name", fullNameId.keys())

        if name:
            student = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
        if st.button(f"Delete {name}") and name and student:
            student.delete()
            logger.info(f"Student {student.fullName} deleted by {current_user.fullName}")
            st.success(f"{student.fullName} deleted successfully")
            st.dataframe(pd.DataFrame([student.to_dict()]))

try:
    delete_student()
except Exception as e:
    logger.error(f"Error in deleting student: {e}")
    st.error("An error occurred while deleting the student.")