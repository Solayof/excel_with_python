#!/usr/bin/python3
from io import BytesIO, StringIO
import logging
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from models import storage
from backup.student_readers import getAllStudents
from backup.getclass import get_classes



from models.portal.admission import Admission
from models.portal.Class import Class

from models.portal.student import Student
from models.portal.subject import Subject
from models.portal.department import Department
from models.portal.teacher import Teacher
from models.portal.user import User
from models.portal.session import Session
from models.portal.admin import Admin
from pages import session_auth

from utils.login import login
from utils.logout import logout

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    storage.create_table()


def viewStream():
    st.set_page_config(
        page_title="CHS BROADSHEET",
        layout="wide"
    )
    st.title("COMPREHENSIVE HIGH SCHOOL IGBOPE")
    st.title("Broadsheet Database")
    current_user = session_auth.current_user()
    
    if not current_user:
        if login():
            st.rerun()
    else:
        st.success(f"Welcome {current_user.fullName}")
        if st.button("Logout"):
            logout()
            logger.info(f"User {current_user.fullName} logged out")
            st.rerun()
    if "session_id" in st.session_state:
        lastname = st.text_input("Search by Last Name")

        if lastname:
            students = Student.search_by_last_name(lastname)
            for stud in students:
                st.write(f"{stud.fullName} - {stud.admission_no} - Class: {stud.classroom.className if stud.classroom else 'N/A'}")
        
        adm_no = st.text_input("Search by Admission Number")

        if adm_no:
            students = Student.search_by_admission_no(adm_no)
            for stud in students:
                st.write(f"{stud.fullName} - {stud.admission_no} - Class: {stud.classroom.className if stud.classroom else 'N/A'}")
        st.selectbox("List of student in Database", [s.fullName for s in Student.query.all()])
 
viewStream()

# depart = Department()
# depart.name = "GENERAL"
# depart.save()


# for clss in get_classes():
#     new_class = Class()
#     new_class.arm = clss.arm
#     new_class.id = clss.id
#     new_class.className = clss.className
#     new_class.code = clss.code
#     new_class.session = clss.session
#     new_class.department_id = depart.id
#     new_class.save()

# for stud in getAllStudents():
#     student = Student()
#     student.firstName = stud.firstName
#     student.lastName = stud.lastName
#     student.middleName = stud.middleName
#     student.admission_no = stud.admission_no
#     student.classroom_id = stud.classroom_id
#     student.gender = stud.gender
#     student.username = stud.admission_no
#     student.email = stud.admission_no
#     student.password = stud.admission_no
#     student.save()
 