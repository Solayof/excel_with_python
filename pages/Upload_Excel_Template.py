#!/usr/bin/python3
from datetime import datetime
from io import BytesIO, StringIO
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
st.title("View Student Subject Score")


def upload_Excel_template():
    excel_file = st.file_uploader("Upload CSV file", type="xlsx")
    data = None
    requiured_cols = {
        "ID",
        "FULL_NAME",
        "CA",
        "EXAM_SCORE"
    }
    if excel_file:
        code = None
        clss = None
        df = pd.read_excel(excel_file)
        st.dataframe(df)
        dic = df.to_dict()
        if not requiured_cols.issubset(df.columns):
            st.error(f"Excel must have columns: {', '.join(requiured_cols)}")
            return
        code = st.selectbox("Class", getClassrooms())
        if code:
            clss = Class.query.filter_by(code=code).one_or_none()
            term_lists = term_list()
            term = st.selectbox("Term", term_lists, index=term_lists.index(current_term()))
            subjects = getclassSubjects(code)
            subjectname = st.selectbox("Subject", subjects)

        # for d in df["ID"]:
        #     dff = df[["ID"]==[d]]
        #     df.iterrows
        #     print(dff)

        for row in df.iterrows():
            dic = list(row)
            print(dic)
        


upload_Excel_template()
