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

def logout():
    if "session_id" in st.session_state:
        session_auth.destroy_session()
        del st.session_state["session_id"]
        st.success("Logged out successfully")
    else:
        st.info("No active session found")