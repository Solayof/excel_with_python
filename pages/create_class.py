#!/usr/bin/python3
from io import BytesIO, StringIO
import logging
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import departs_name_with_id, getClassrooms, getClassroom, getStudentById, getStudentsIdandNames, getclassSubjects
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
st.title("Add Class")

def create_class():
    room = st.selectbox("classroom", ["JSS 1", "JSS 2", "JSS 3", 'SSS 1', 'SSS 2', 'SSS 3'])
    arm = st.selectbox("Arms", ["A", "B", "C", "D", "E"])
    departs_dict = departs_name_with_id()
    name = st.selectbox("Department", departs_dict.keys())
    depart_id = departs_dict.get(name, None) if name else None
    if st.button('Add class') and arm and room:
        clss = Class(className=room, arm=arm)
        clss.department_id = depart_id
        if  getClassroom(clss.code):
            st.warning(f"class {clss.code} exists")
            return
        clss.save()
        logger.info(f"class {clss.code} created by {current_user.fullName}")
        st.success(f"class {clss.code} created successfully")

try:
    create_class()
except Exception as e:
    logger.error(f"Error in creating class: {e}")
    st.error("An error occurred while creating the class.")
    