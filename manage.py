#!/usr/bin/python3
from io import BytesIO
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
    menu = st.sidebar.selectbox("Menu", ["Add class", "Add student", "Upload score", "Generate sheet", "Download sheet"])

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
        st.info("Please ensure not two students with the same full name are the same arm")
        st.info("Please enter the form manually dont autofill")
        code = st.selectbox("Class", Class.all())
        if code:
            clss = Class.query.filter_by(code=code).one()
        firstName = st.text_input("First Name", placeholder="First Name")
        middleName = st.text_input("Middle Name", placeholder="Middle Name")
        lastName = st.text_input("Last Name", placeholder="last Name")
        admission_Number = st.text_input("Admission Number", placeholder="Admission Number")
        gender = st.selectbox("Gender", ["Male", "Female"])
        if st.button("Add student") and firstName and lastName and admission_Number and clss:

            stud = Student()
            stud.firstName = firstName.upper()
            stud.middleName = middleName.upper()
            stud.lastName = lastName.upper()
            stud.admission_no = admission_Number.upper()
            stud.gender = gender
            stud.classroom_id = clss.id
            stu = Admission.query.filter(Admission.admission_no==stud.admission_no).one_or_none()
            if stu:
                st.error(f"{stu.fullName} has {admission_Number} as admission number")
                return
            stud.save()
            st.success(f"{stud.fullName} created successfuly with id: {stud.id}")


    if menu == "Upload score":
        st.header("Upload Scores")
        code = st.selectbox("Class", Class.all())
        subjectlist = []
        stdlist = []
    
        if code:
            clss = Class.query.filter_by(code=code).one()
            subjectlist = clss.sheetSubjects
            students = clss.students
            stdlist = [std.fullName for std in students]

        name = st.selectbox("Name", stdlist)
        subjectname = st.selectbox("Subject", subjectlist)
        ca = st.number_input("Continuous Assessment", 0, 30)
        exam = st.number_input("Third Term Score", 0, 70)
        firstTermScore = st.number_input("First Term Score", 0, 100)
        secondTermScorce = st.number_input("Third Term Score", 0, 100)

        if st.button("upload score") and name and subjectname and ca and exam and firstTermScore and secondTermScorce:
            for std in students:
                if std.fullName == name:
                    std_id = std.id
            
            subject = Subject()
            subject.name = subjectname
            subject.student_id = std_id
            subject.CA = ca
            subject.firstTermScore = firstTermScore
            subject.secondTermScore = secondTermScorce
            subject.examScore = exam
            if not subject.student_id:
                st.error("score can not be save, no student attached")
            subject.save()
            st.success("score save successfully")

    if menu == "Generate sheet":
        st.header("Generate Sheet")
        code = st.selectbox("Class", Class.all())
        if code:
            clss = Class.query.filter_by(code=code).one()
        if st.button("Generate Sheet") and clss:
            clss.generateSheet()
            st.success(f"sheet with file name: {code}.xlsx generated successfully")

    if menu == "Download sheet":
        st.header("Download Sheet")
        code = st.selectbox("Class", Class.all())
        if code:
            clss = Class.query.filter_by(code=code).one()

            try:
                with open(f"{clss.code}.xlsx", "rb") as file:
                    st.download_button(
                        label=f"Download {clss.code}.xlsx file",
                        data=file,
                        file_name=f"{clss.code}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
            except FileNotFoundError:
                st.error("Generate sheet for the class first")
            

        



viewStream()