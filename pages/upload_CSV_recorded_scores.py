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

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User

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


def upload_CSV_record():
    csv_text = st.text_area("Past your csv text here")
    csv_file = st.file_uploader("Upload CSV file", type="csv")
    data = None
    requiured_cols = {
        "FULLNAME",
        "CA",
        "EXAM_SCORE",
        "FIRST_TERM_SCORE",
        "SECOND_TERM_SCORE"
    }
    if st.button("Upload") and csv_text:
        try:
            data = pd.read_csv(StringIO(csv_text))
        except Exception as e:
            st.warning("eerror")
    elif csv_file:
        data = pd.read_csv(csv_file)
    if isinstance(data, pd.DataFrame):
        if not requiured_cols.issubset(data.columns):
            st.error(f"CSV must have columns: {', '.join(requiured_cols)}")
            return
        name_list = data["FULLNAME"].unique()
        print(name_list)
        

        
        st.dataframe(pd.DataFrame([name_list]))
        
        code = st.selectbox("Class", getClassrooms())
    
        if code:
            fullNameId = getStudentsIdandNames(code)
            for name in name_list:
                if name in fullNameId.keys():
                    student_data = data[data["FULLNAME"] == "SOLOMON"].iloc[0].to_dict()
                    st.dataframe(pd.DataFrame([student_data]))
                    subject = Subject()
                    subject.student_id = fullNameId[name]

                    if student_data.get("CA", 0) <= 30:
                        subject.CA = student_data.get("CA", 0)
                    if student_data.get("EXAM_SCORE", 0) <= 70:
                        subject.examScore = student_data.get("EXAM_SCORE", 0)
                    if student_data.get("FIRST_TERM_SCORE", 0):
                        subject.firstTermScore = student_data.get("FIRST_TERM_SCORE", 0)
                    if student_data.get("SECOND_TERM_SCORE", 0):
                        subject.secondTermScore = student_data.get("SECOND_TERM_SCORE", 0)
                    subject.save()
                else:
                    st.warning(f"{name} is not a student of {code}")

upload_CSV_record()