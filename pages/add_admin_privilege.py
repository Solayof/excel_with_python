#!/usr/bin/python3
import datetime
from io import BytesIO, StringIO
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy.orm.attributes import flag_modified

from models.cache import getClassrooms, getClassroom, getStudentById, getStudentsIdandNames, getclassSubjects, departs_name_with_id, teacher_name_id
from models.portal.admission import Admission
from models.portal.Class import Class
from models.portal.department import Department

from models.portal.student import Student
from models.portal.subject import Subject
from models.portal.admin import Admin

from models.portal.user import User
from pages import session_auth

current_user = session_auth.current_user()
if not current_user:
    st.switch_page("CHS_IGBOPE_PORTAL.py")
if current_user.isAdmin() is False:
    st.switch_page("CHS_IGBOPE_PORTAL.py")

st.set_page_config(
    page_title="Add Admin Privileges",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an app to manage student result"
    }
)
st.title("Add Admin Privileges")

def admin_privileges():
    teacher_dict = teacher_name_id()
    all_privileges = [
            "create",
            "delete",
            "update",
            "superadmin"
        ]
    if teacher_dict:
        name = st.selectbox("Name", teacher_dict.keys())
        privileges = st.multiselect("Grant privileges", all_privileges)

        if st.button("Grant Privileges") and name:
            admin = Admin.query.filter_by(teacher_id=teacher_dict[name]).one_or_none()
            if not admin:
                admin = Admin(teacher_id=teacher_dict[name])
            for privilege in all_privileges:
                if privilege in privileges:
                    admin.privileges[privilege] = True
                else:
                    admin.privileges[privilege] = False
            flag_modified(admin, "privileges")
            adm = Admin.query.filter_by(teacher_id=current_user.id).one()
            if adm.privileges.get("superadmin") is False:
                st.error("Permission Denial")
                return
            admin.save()
            st.success("Privileges granted")
            

admin_privileges()