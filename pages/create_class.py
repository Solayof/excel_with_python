#!/usr/bin/python3
from io import BytesIO, StringIO
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import getClassrooms, getClassroom, getStudentById, getStudentsIdandNames, getclassSubjects
from models.portal.admission import Admission
from models.portal.Class import Class

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User

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
    if st.button('Add class') and arm and room:
        clss = Class(className=room, arm=arm)
        if  getClassroom(clss.code):
            st.warning(f"class {clss.code} exists")
            return
        clss.save()
        st.success(f"class {clss.code} created successfully")

create_class()
    