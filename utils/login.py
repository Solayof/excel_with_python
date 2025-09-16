#!/usr/bin/python3
import datetime
from io import BytesIO, StringIO
import numpy as np
from sqlalchemy import or_
import streamlit as st
import pandas as pd
import plotly.express as px

from models.cache import getClassrooms, getClassroom, getStudentById, getStudentsIdandNames, getclassSubjects, departs_name_with_id
from models.portal.teacher import Teacher
from models.portal.department import Department
from models.portal.user import User
from pages import session_auth

def login():

    username = st.text_input("Username", placeholder="Username")
    password = st.text_input("Password", placeholder="Password", type="password")
    if st.button("Login") and username and password:

        user = User.query.filter(or_(User.username == username, User.email == username)).one_or_none()
        if user and user.is_valid_password(password):
            session_id = session_auth.create_session(user.id)
            st.session_state["session_id"] = session_id
            st.success("Login successful")
            return True
        else:
            st.error("Invalid username or password")
            return False