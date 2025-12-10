#!/usr/bin/python3
from datetime import datetime
from io import BytesIO, StringIO
from openpyxl import Workbook
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import (getClassrooms)
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
    page_title="Download Excel Recording Template",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an app to manage student result"
    }
)
st.title("Recording Template")



def template_sheet():
        code = st.selectbox("Class", getClassrooms())
        wb = Workbook()
        clss = None
        if code:
            clss = Class.query.filter_by(code=code).one_or_none()
        if st.button("Generate Template") and clss:
            ws = wb.active
            ws.title = code
            ws.append(["ID", "FULL_NAME", "CA", "EXAM_SCORE"])
            for student in clss.students:
                 ws.append([student.admission_no, student.fullName])
            wb.save(f"template-{code}.xlsx")
            st.success(f"sheet with file name: template-{code}.xlsx generated successfully")
        try:
            with open(f"template-{clss.code}.xlsx", "rb") as file:
                st.download_button(
                    label=f"Download template-{clss.code}.xlsx file",
                    data=file,
                    file_name=f"template-{clss.code}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"
                )
                
        except FileNotFoundError:
            st.error("Generate sheet for the class first")

template_sheet()