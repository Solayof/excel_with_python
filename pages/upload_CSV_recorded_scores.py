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

def upload_CSV_record():
    st.subheader("Upload Student Subject Scores")

    csv_text = st.text_area("Paste your CSV text here")
    csv_file = st.file_uploader("Or upload CSV file", type="csv")

    required_cols = {"ID", "FULL_NAME", "CA", "EXAM_SCORE"}
    data = None

    if csv_text:
        data = StringIO(csv_text)
    elif csv_file:
        data = csv_file

    if not data:
        return

    try:
        df = pd.read_csv(data, dtype={"ID": str})
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

    except Exception as e:
        st.error(f"CSV read error: {e}")
        return

    st.dataframe(df, use_container_width=True)

    if not required_cols.issubset(df.columns):
        st.error(f"CSV must contain columns: {', '.join(required_cols)}")
        return

    # Selections
    class_code = st.selectbox("Class", getClassrooms())
    if not class_code:
        return

    clss = Class.query.filter_by(code=class_code).one_or_none()
    if not clss:
        st.error("Invalid class selected")
        return

    terms = term_list()
    selected_term = st.selectbox(
        "Term",
        terms,
        index=terms.index(current_term())
    )

    subjects = getclassSubjects(class_code)
    subject_name = st.selectbox("Subject", subjects)

    if not st.button("Upload Scores"):
        return

    # Upload loop
    for row in df.itertuples(index=False):
        if row.CA < 0 or row.CA > 30:
            st.error(f"Invalid CA ({row.CA}) for ID {row.ID}")
            continue

        if row.EXAM_SCORE < 0 or row.EXAM_SCORE > 70:
            st.error(f"Invalid EXAM score ({row.EXAM_SCORE}) for ID {row.ID}")
            continue
        std = Student.query.filter_by(admission_no=row.ID).one_or_none()

        if not std:
            st.error(f"Student with admission number {row.ID} not found")
            continue

        if std.classroom_id != clss.id:
            st.error(f"{std.fullName} is not in {class_code}")
            continue

        sub = Subject.query.filter_by(
            name=subject_name,
            student_id=std.id,
            term=selected_term,
            session=current_session(),
        ).one_or_none()

        if not sub:
            sub = Subject(
                name=subject_name,
                student_id=std.id,
                term=selected_term,
                session=current_session(),
                CA=row.CA,
                examScore=row.EXAM_SCORE,
            )
            sub.save()
            st.info(f"Scores added for {std.fullName}")
        else:
            sub.CA = row.CA
            sub.examScore = row.EXAM_SCORE
            sub.save()
            st.info(f"Scores updated for {std.fullName}")

    st.success("Scores uploaded successfully ✅")


upload_CSV_record()
