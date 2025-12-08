import streamlit as st

from models.portal.Class import Class

@st.cache_data(ttl=30000)
def current_term():
    import datetime
    mth = int(datetime.datetime.now().strftime("%m"))
    if mth in [9, 10, 11, 12]:
        return "First Term"
    elif mth in [1, 2, 3, 4]:
        return "Second Term"
    else:
        return "Third Term"
    
@st.cache_data(ttl=30000)
def term_list():
    return ["First Term", "Second Term", "Third Term"]

@st.cache_data(ttl=30000)
def current_session():
    import datetime
    yr = int(datetime.datetime.now().strftime("%y"))
    mth = int(datetime.datetime.now().strftime("%m"))
    if mth < 9:
        yr = yr - 1
    return f"20{yr}-20{yr + 1}"


@st.cache_data(ttl=360)
def getclassSubjects(code):
     clss = Class.query.filter_by(code=code).one_or_none()
     return clss.sheetSubjects
