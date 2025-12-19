#!/usr/bin/python3
from datetime import datetime
from io import BytesIO, StringIO
import logging
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import (getClassrooms,
                          getClassroom,
                          getStudentById,
                          getStudentsIdandNames,
                          getclassSubjects,
                          session_list)
from models.portal.admission import Admission
from models.portal.cache import current_session, current_term, term_list
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
    page_title="Record Student Subject Score",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an app to manage student result"
    }
)
st.title("Download Sheet")



def download_sheet():
    st.header("Download Sheet")
    code = st.selectbox("Class", getClassrooms())
    if code:
        clss = Class.query.filter_by(code=code).one_or_none()
        if st.button("Generate Sheet") and clss:
            clss.generateSheet(term='First Term')
            logger.info(f"Sheet generated for class {code} by {current_user.fullName}")
            st.success(f"sheet with file name: {code}.xlsx generated successfully")

    try:
        with open(f"{code}.xlsx", "rb") as file:
            st.download_button(
                label=f"Download {code}.xlsx file",
                data=file,
                file_name=f"{code}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"
            )
            
    except FileNotFoundError:
        st.error("Generate sheet for the class first")

download_sheet()