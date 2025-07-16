#!/usr/bin/python3
from io import BytesIO
import streamlit as st
import pandas as pd
import plotly.express as px
from models import storage


from models.portal.admission import Admission
from models.portal.Class import Class

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User


if __name__ == "__main__":
    storage.create_table()

def viewStream():
    st.title("COMPREHENSIVE HIGH SCHOOL IGBOPE")
    st.title("Broadsheet Database")
    menu = st.sidebar.selectbox("Menu", [
        "Add class", "Add student", "Edit Student", "Upload score", "Update score",
        "Generate sheet", "Download sheet", "View student scores", "View class", 
        "Delete sudent", "Performance Analytics"
    ])
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
    
        if code:
            clss = Class.query.filter_by(code=code).one()
            
            students = clss.students
            if students:
                students.sort(key=lambda s: s.fullName)
            stdlist = [std.fullName for std in students]
            name = st.selectbox("Name", stdlist)
            for std in students:
                if std.fullName == name:
                    student = std
                    subjectlist = [sub for sub in clss.sheetSubjects if sub not in student.subject_recoeded()]
                    break

       
        subjectname = st.selectbox("Subject", subjectlist)
        ca = st.number_input("Continuous Assessment", 0, 30)
        exam = st.number_input("Third Term Score (Just the exam score)", 0, 70)
        firstTermScore = st.number_input("First Term Score", 0, 100)
        secondTermScorce = st.number_input("Second Term Score", 0, 100)

        if st.button("upload score") and name and subjectname and ca:
            
            if firstTermScore == 0 and secondTermScorce == 0:
                firstTermScore = exam + ca
                secondTermScorce = firstTermScore
            if firstTermScore == 0:
                firstTermScore = round((secondTermScorce + exam + ca) / 2)
            subject = Subject()
            subject.name = subjectname
            subject.student_id = student.id
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


    if menu == "View student scores":
        st.header("Student Scores")

        code = st.selectbox("Class", Class.all())
        stdlist = []
    
        if code:
            clss = Class.query.filter_by(code=code).one()
            students = clss.students
            if not students:
                return
            students.sort(key=lambda s: s.fullName)
            stdlist = [std.fullName for std in students]

            name = st.selectbox("Name", stdlist)

            for std in students:
                    if std.fullName == name:
                        student = std
                        break

            subjects = student.subjects_to_dict()
            df = pd.DataFrame(subjects)
            
            if subjects:
                st.dataframe(df)
                sub_analysis = [
                    {
                        "Subject": name,
                        "Average Score": sum(sub.values()) / 3
                    } for name, sub in subjects.items()
                ]
                subdf = pd.DataFrame(sub_analysis)
                fig = px.bar(subdf, x="Subject", y="Average Score", 
                                    title=f"Class {code} - {student.fullName}",
                                    labels={"Average Score": "Avg Score"}, 
                                    color="Average Score", height=500)
                st.plotly_chart(fig, use_container_width=True)
    
    if menu == "View class":
        st.title("View Classes")
        code = st.selectbox("Class", Class.all())
        stdlist = []
    
        if code:
            clss = Class.query.filter_by(code=code).one()

            df = pd.DataFrame(clss.students_to_dict())

            st.dataframe(df)



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
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"
                    )
                    
            except FileNotFoundError:
                st.error("Generate sheet for the class first")


    if menu == "Delete sudent":
        st.header("Delete Students")
        code = st.selectbox("Class", Class.all())
     
        stdlist = []
    
        if code:
            clss = Class.query.filter_by(code=code).one()
            subjectlist = clss.sheetSubjects
            students = clss.students
            if students:
                students.sort(key=lambda s: s.fullName)
            stdlist = [std.fullName for std in students]
        if stdlist:
            st.info("Select a student to delete")
            name = st.selectbox("Name", stdlist)
            if st.button(f"Delete {name}") and name and students:
                for std in students:
                    if std.fullName == name:
                        std.delete()
                        st.success(f"{std.fullName} deleted successfully")
                        st.dataframe(pd.DataFrame([std.to_dict()]))
                        break
    

    if menu == "Edit Student":
        st.header("Edit Students")
        code = st.selectbox("Class", Class.all())
     
        stdlist = []
    
        if code:
            clss = Class.query.filter_by(code=code).one()
            students = clss.students
            if students:
                students.sort(key=lambda s: s.fullName)
            stdlist = [std.fullName for std in students]

        name = st.selectbox("Name", stdlist)
        
        if name:
            for std in students:
                if std.fullName == name:
                        stud = std
                        
                        break

            if stud:
                firstName = st.text_input("First Name", placeholder="First Name", value=stud.firstName)
                middleName = st.text_input("Middle Name", placeholder="Middle Name", value=stud.middleName)
                lastName = st.text_input("Last Name", placeholder="last Name", value=stud.lastName)
                admission_Number = st.text_input("Admission Number", placeholder="Admission Number", value=stud.admission_no)
                gender = st.selectbox("Gender", ["Male", "Female"])

            if st.button("Update student") and stud:
                stud.firstName = firstName.upper()
                stud.middleName = middleName.upper()
                stud.lastName = lastName.upper()
                stud.admission_no = admission_Number.upper()
                stud.gender = gender

                stud.save()
                st.dataframe(pd.DataFrame([stud.to_dict()]))
                st.success("Updated successfuly")

    if menu == "Performance Analytics":
        st.header("📈 Performance Analytics")
        code = st.selectbox("Select Class", Class.all())

        if code:
            clss = Class.query.filter_by(code=code).one()
            students = clss.students

            if not students:
                st.warning("No students found in this class.")
            else:
                # Collect student performance
                performance_data = []
                for student in students:
                    scores = student.subjects_to_dict()
                    if scores:
                        total_score = sum([sum(sub.values())/3 for sub in scores.values()])
                        avg_score = total_score / len(scores)
                        performance_data.append({
                            "Name": student.fullName,
                            "Average Score": avg_score,
                        })

                if performance_data:
                    df_perf = pd.DataFrame(performance_data).sort_values(by="Average Score", ascending=False)

                    # Grade Distribution
                    def grade(score):
                        if score >= 70: return "A"
                        elif score >= 60: return "B"
                        elif score >= 50: return "C"
                        elif score >= 40: return "D"
                        else: return "F"
                    st.subheader("Average Scores Per Student")
                    df_perf["Grade"] = df_perf["Average Score"].apply(grade)
                    st.dataframe(df_perf)

                    # Bar chart for average scores
                    fig = px.bar(df_perf, x="Name", y="Average Score", 
                                title=f"Class {code} - Average Performance",
                                labels={"Average Score": "Avg Score"}, 
                                color="Average Score", height=500)
                    st.plotly_chart(fig, use_container_width=True)

                    

                    grade_dist = df_perf["Grade"].value_counts().reset_index()
                    grade_dist.columns = ["Grade", "Count"]

                    st.subheader("Grade Distribution")
                    fig2 = px.pie(grade_dist, names="Grade", values="Count", title="Grade Breakdown")
                    st.plotly_chart(fig2)

    if menu == "Update score":
        st.header("Update Scores")
        code = st.selectbox("Class", Class.all())
    
        if code:
            clss = Class.query.filter_by(code=code).one()
            students = clss.students
            if students:
                students.sort(key=lambda s: s.fullName)
            stdlist = [std.fullName for std in students]
            name = st.selectbox("Name", stdlist)
            
            if name:
                for std in students:
                    if std.fullName == name:
                            stud = std
                            break
                subjectlist = [sub for sub in clss.sheetSubjects if sub in stud.subject_recoeded()]
                subjectname = st.selectbox("Subject", subjectlist)
        
                subject = Subject.query.filter_by(student_id=stud.id, name=subjectname).one_or_none()
                if stud and subject:
                    ca = st.number_input("Continuous Assessment", 0, 30, subject.CA)    
                    exam = st.number_input("Third Term Score", 0, 70, subject.examScore)
                    firstTermScore = st.number_input("First Term Score", 0, 100, subject.firstTermScore)
                    secondTermScorce = st.number_input("Second Term Score", 0, 100, subject.secondTermScore)
                    
                    if st.button("Update"):
                        if firstTermScore == 0 and secondTermScorce == 0:
                            firstTermScore = exam + ca
                            secondTermScorce = firstTermScore
                        if firstTermScore == 0:
                            firstTermScore = round((secondTermScorce + exam + ca) / 2)

                        subject.CA = ca
                        subject.examScore = exam
                        subject.firstTermScore = firstTermScore
                        subject.secondTermScore = secondTermScorce
                        subject.save()

                        st.success("score updated successfully")




        # arisekola77



viewStream()