#!/usr/bin/python3
import streamlit as st
import pandas as pd
from models import storage


from models.portal.admission import Admission
from models.portal.Class import Class

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User


if __name__ == "__main__":
    storage.create_table()

def viewStream():
    st.title("Broadsheet Database")
    menu = st.sidebar.selectbox("Menu", ["Add class", "Add student", "Add subject"])

    if menu == "Add class":
        st.header("Add Classes")
        room = st.selectbox("classroom", ["JSS 1", "JSS 2", "JSS 3", 'SSS 1', 'SSS 2', 'SSS 3'])
        arm = st.selectbox("Arms", ["A", "B", "C", "D", "E"])
        if st.button('Add class') and arm and room:
            clss = Class(className=room, arm=arm)
            if Class.query.filter_by(code=clss.code).one_or_none():
                st.warning(f"class {clss.code} exists")
                return
            clss.save()
            st.success(f"class {clss.code} created successfully")
    
    if menu == "Add student":
        st.header("Add Students")
        firstName = st.text_input("First Name", placeholder="First Name")
        middleName = st.text_input("Middle Name", placeholder="Middle Name")
        lastName = st.text_input("Last Name", placeholder="last Name")
        admission_Number = st.text_input("Admission Number", placeholder="Admission Number")
        gender = st.selectbox("Gender", ["Male", "Female"])
        print("here", lastName, firstName, middleName, admission_Number)
        if st.button("Add student") and firstName and lastName and admission_Number:

            stud = Student()
            stud.firstName = firstName.upper()
            stud.middleName = middleName.upper()
            stud.lastName = lastName.upper()
            stud.admission_no = admission_Number.upper()
            stud.gender = gender
            stu = Admission.query.filter(Admission.admission_no==stud.admission_no).one_or_none()
            if stu:
                st.error(f"{stud.fullName} has {admission_Number} as admission number")
                return
            stud.save()
            st.success(f"{stud.fullName} created successfuly with id: {stud.id}")
        st.info("please enter the form manually dont autofill")



viewStream()