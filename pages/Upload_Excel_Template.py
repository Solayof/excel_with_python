#!/usr/bin/python3
from datetime import datetime
from io import BytesIO, StringIO
import logging
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import (getClassrooms,
                          getClassroom, getCurrentClassrooms,
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
        df = pd.read_excel(excel_file, dtype={"ID": str})
        df.columns = df.columns.str.strip().str.upper()
        df["ID"] = df["ID"].astype(str).str.strip()
        MAX_CA = 30
        MAX_EXAM = 70

        # Convert to numeric (invalid values become NaN)
        df["CA"] = pd.to_numeric(df["CA"], errors="coerce")
        df["EXAM_SCORE"] = pd.to_numeric(df["EXAM_SCORE"], errors="coerce")

        # Check for invalid values
        invalid_rows = df[
            (df["CA"].isna()) |
            (df["EXAM_SCORE"].isna()) |
            (df["CA"] < 0) |
            (df["CA"] > MAX_CA) |
            (df["EXAM_SCORE"] < 0) |
            (df["EXAM_SCORE"] > MAX_EXAM)
        ]
        if not invalid_rows.empty:
            st.error("Some rows have invalid CA or EXAM_SCORE values")
            st.dataframe(invalid_rows)
            st.stop()

        st.dataframe(df)
        if not requiured_cols.issubset(df.columns):
            st.error(f"Excel must have columns: {', '.join(requiured_cols)}")
            return
        code = st.selectbox("Class", getCurrentClassrooms())
        if code:
            clss = Class.query.filter_by(code=code).one_or_none()
            term_lists = term_list()
            term = st.selectbox("Term", term_lists, index=term_lists.index(current_term()))
            subjects = getclassSubjects(code)
            subjectname = st.selectbox("Subject", subjects)
        if st.button("Upload Scores"):
            for row in df.itertuples(index=False):
                if row.CA < 0 or row.CA > 30:
                    st.error(f"Invalid CA ({row.CA}) for ID {row.ID}")
                    continue

                if row.EXAM_SCORE < 0 or row.EXAM_SCORE > 70:
                    st.error(f"Invalid EXAM score ({row.EXAM_SCORE}) for ID {row.ID}")
                    continue
                std = Student.query.filter_by(admission_no=row.ID).one_or_none()
                if std is None:
                    st.error(f"Student with admission number {row.ID} not found")
                    continue
                if std.classroom_id != clss.id:
                    st.error(f"Student {std.fullName} not in class {code}")
                    continue
                sub  = Subject.query.filter_by(
                    name=subjectname,
                    student_id=std.id,
                    term=term,
                    ).one_or_none()
                if sub is None:
                    sub = Subject(
                        name=subjectname,
                        student_id=std.id,
                        term=term,
                        session=current_session(),
                        CA=row.CA,
                        examScore=row.EXAM_SCORE,
                    )
                    sub.save()
                    logger.info(f"Scores for {std.fullName} in subject {subjectname} added in class {code} for term {term} session {current_session()} by {current_user.fullName}")
                    st.info(f"Scores for {std.fullName} added")
                else:
                    sub.CA = row.CA
                    sub.examScore = row.EXAM_SCORE
                    sub.save()
                    st.info(f"Scores for {std.fullName} updated")
                    logger.info(f"Scores for {std.fullName} in subject {subjectname} updated in class {code} for term {term} session {current_session()} by {current_user.fullName}")
            logger.info(f"Scores for subject {subjectname} in class {code} for term {term} session {current_session()} uploaded by {current_user.fullName}")
            st.success("Scores uploaded successfully")    


upload_Excel_template()
