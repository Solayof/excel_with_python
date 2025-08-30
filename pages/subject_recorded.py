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


def subject_recorded():
    st.header("Subject Recorded")
    code = st.selectbox("Class", getClassrooms())
    subject = None
    if code:
        clss =  getClassroom(code)
        students = Student.query.filter_by(classroom_id=clss.id).all()
        subjectlist = [sub for sub in getclassSubjects(code)]
        subjectname = st.selectbox("Subject", subjectlist)
        studentlist = []
        for stud in students:
            obj = {}
            subject = Subject.query.filter_by(student_id=stud.id, name=subjectname).one_or_none()
            if subject:
                obj["FULLNAME"] = stud.fullName
                obj["CA"] = subject.CA
                obj["EXAM SCORE"] = subject.examScore
                obj["FIRST TERM SCORE"] = subject.firstTermScore
                obj["SECOND TERM SCORE"] = subject.secondTermScore
                obj["AVERAGE SCORE"] = (subject.CA + subject.examScore + subject.firstTermScore + subject.secondTermScore) / 3
            else:
                obj["FULLNAME"] = stud.fullName
            studentlist.append(obj)

        stdf = pd.DataFrame(studentlist)
        st.dataframe(stdf.sort_values(by="AVERAGE SCORE", ascending=False))
        if subject:
            pldf = stdf[["FULLNAME", "AVERAGE SCORE"]]
            fig = px.bar(pldf, x="FULLNAME", y="AVERAGE SCORE", 
                title=f"Class {code} {subjectname}- Average Performance",
                labels={"AVERAGE SCORE": "Avg Score"}, 
                color="AVERAGE SCORE", height=500)
            st.plotly_chart(fig, use_container_width=True)
           
