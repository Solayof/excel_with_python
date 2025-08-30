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


def report_sheet():
    st.header("Report Sheet")
    code = st.selectbox("Class", getClassrooms())

    if code:
        fullNameId = getStudentsIdandNames(code)
        name = st.selectbox("Name", fullNameId.keys())
        if name:
            stud = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
        if stud:
            subjects = stud.subjects
            subjectList = []
            for sub in subjects:
                obj = {}
                obj["Subject"] = sub.name
                obj["CA"] = sub.CA
                obj["EXAM SCORE"] = sub.examScore
                obj["FIRST TERM SCORE"] = sub.firstTermScore
                obj["SECOND TERM SCORE"] = sub.secondTermScore
                subjectList.append(obj)
            subjectlist = [sub for sub in getclassSubjects(code) if sub not in stud.subject_recoeded()]
            for sub in subjectlist:
                obj = {}
                obj["Subject"] = sub
                subjectList.append(obj)
                df = pd.DataFrame(subjectList)
            df["TOTAL"] = df[["CA", "EXAM SCORE", "FIRST TERM SCORE", "SECOND TERM SCORE"]].sum(axis=1)
            st.dataframe(df.sort_values(by="TOTAL", ascending=False))

report_sheet()