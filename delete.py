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

students = Student.search_by_last_name("thomas")
for stud in students:
    if not stud.subjects:
        print(f"{stud.fullName} - {stud.admission_no} - Class: {stud.classroom.className if stud.classroom else 'N/A'}")