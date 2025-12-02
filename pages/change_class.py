#!/usr/bin/python3
from io import BytesIO, StringIO
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
st.title("Change Class or Promote Student")
def change_class():
    code = None
    code = st.selectbox("Class", getClassrooms())
    stud = None
    name = None
    if code:
        fullNameId = getStudentsIdandNames(code)
        if fullNameId:
            name = st.selectbox("Name", fullNameId.keys())

        if name:
            stud = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
    class_to_code = st.selectbox("Class To", [room for room in getClassrooms() if room != code])
    if class_to_code:
        clss_to = Class.query.filter_by(code=class_to_code).one()

        if st.button("Change Class") and stud and clss_to:
            stud.classroom_id = clss_to.id
            stud.save()
            st.table(pd.DataFrame([stud.to_dict()]))
            st.success("Class changed successfully")

change_class()