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

def view_student_score():
    st.header("Student Scores")

    code = st.selectbox("Class", getClassrooms())

    if code:
        fullNameId = getStudentsIdandNames(code)
        name = st.selectbox("Name", fullNameId.keys())

        if name:
            student = Student.query.filter_by(id=fullNameId[name]).one_or_none()
        if student:
            subjects = student.overall_subjects_scores()
            df = pd.DataFrame(subjects)
        
            if subjects:
                st.dataframe(df)
                sub_analysis = [
                    {
                        "Subject": name,
                        "Average Score": sum(sub.values())
                    } for name, sub in subjects.items()
                ]
                subdf = pd.DataFrame(sub_analysis)
                fig = px.bar(subdf, x="Subject", y="Average Score", 
                                    title=f"Class {code} - {student.fullName}",
                                    labels={"Average Score": "Avg Score"}, 
                                    color="Average Score", height=500)
                st.plotly_chart(fig, use_container_width=True)
    
view_student_score()