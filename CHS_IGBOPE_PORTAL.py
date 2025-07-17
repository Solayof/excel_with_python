#!/usr/bin/python3
from io import BytesIO, StringIO
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
@st.cache_data(ttl=5000)
def getClassrooms():
    return Class.all()

@st.cache_data(ttl=5000)
def getStudentsIdandNames(code):
    clss = Class.query.filter_by(code=code).one_or_none()
    return clss.getStudentsIdandNames()

@st.cache_data(ttl=5000)
def getclassSubjects(code):
     clss = Class.query.filter_by(code=code).one_or_none()
     return clss.sheetSubjects

@st.cache_data(ttl=60000)
def getClassroom(code):
    return Class.query.filter_by(code=code).one_or_none()

@st.cache_data(ttl=30000)
def getStudentById(id):
    return Student.query.filter_by(id=id).one_or_none()

def viewStream():
    st.title("COMPREHENSIVE HIGH SCHOOL IGBOPE")
    st.title("Broadsheet Database")
    menu = st.sidebar.selectbox("Menu", [
        "Add class", "Add student", "Edit Student", "Change Student Class", "Upload score", "Update score", "Subject Recorded",
        "Generate sheet", "Download sheet", "View student scores", "View class", "Upload CSV Record", "Delete Students Score",
        "Delete sudent", "Performance Analytics"
    ])
    if menu == "Add class":
        st.header("Add Classes")
        room = st.selectbox("classroom", ["JSS 1", "JSS 2", "JSS 3", 'SSS 1', 'SSS 2', 'SSS 3'])
        arm = st.selectbox("Arms", ["A", "B", "C", "D", "E"])
        if st.button('Add class') and arm and room:
            clss = Class(className=room, arm=arm)
            if  getClassroom(clss.code):
                st.warning(f"class {clss.code} exists")
                return
            clss.save()
            st.success(f"class {clss.code} created successfully")
    
    if menu == "Add student":
        st.header("Add Students")
        st.info("Please ensure not two students with the same full name are the same arm")
        st.info("Please enter the form manually dont autofill")
        code = st.selectbox("Class", getClassrooms())
        if code:
            clss =  getClassroom(code)
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
        code = st.selectbox("Class", getClassrooms())
    
        if code:
            fullNameId = getStudentsIdandNames(code)
            name = st.selectbox("Name", fullNameId.keys())
            if name:
                student = Student.query.filter_by(id=fullNameId[name]).one_or_none()
                subjectlist = [sub for sub in getclassSubjects(code) if sub not in student.subject_recoeded()]
       
                subjectname = st.selectbox("Subject", subjectlist)
        ca = st.number_input("Continuous Assessment", 0, 30)
        exam = st.number_input("Third Term Score (Just the exam score)", 0, 70)
        firstTermScore = st.number_input("First Term Score", 0, 100)
        secondTermScorce = st.number_input("Second Term Score", 0, 100)

        if st.button("upload score") and name and subjectname:
            
            if firstTermScore == 0 and secondTermScorce == 0 and exam and ca:
                firstTermScore = exam + ca
                secondTermScorce = firstTermScore
            if firstTermScore == 0 and exam and ca and secondTermScorce:
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
        code = st.selectbox("Class", getClassrooms())
        if code:
            clss = getClassroom(code)
        if st.button("Generate Sheet") and clss:
            clss.generateSheet()
            st.success(f"sheet with file name: {code}.xlsx generated successfully")


    if menu == "View student scores":
        st.header("Student Scores")

        code = st.selectbox("Class", getClassrooms())
        stdlist = []
    
        if code:
            fullNameId = getStudentsIdandNames(code)
            name = st.selectbox("Name", fullNameId.keys())

            if name:
                student = Student.query.filter_by(id=fullNameId[name]).one_or_none()
            if student:
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
        code = st.selectbox("Class", getClassrooms())
    
        if code:
            clss =  getClassroom(code)

            df = pd.DataFrame(clss.students_to_dict())

            st.dataframe(df)



    if menu == "Download sheet":
        st.header("Download Sheet")
        code = st.selectbox("Class", getClassrooms())
        if code:
            clss =  getClassroom(code)

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


    if menu == "Delete student":
        st.header("Delete Students")
        code = st.selectbox("Class", getClassrooms())
    
        if code:
            fullNameId = getStudentsIdandNames(code)
            st.info("Select a student to delete")
            name = st.selectbox("Name", fullNameId.keys())

            if name:
                student = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
            if st.button(f"Delete {name}") and name and student:
                student.delete()
                st.success(f"{student.fullName} deleted successfully")
                st.dataframe(pd.DataFrame([student.to_dict()]))
    

    if menu == "Edit Student":
        st.header("Edit Students")
        code = st.selectbox("Class", getClassrooms())

        if code:
            fullNameId = getStudentsIdandNames(code)
            name = st.selectbox("Name", fullNameId.keys())

        if name:
            stud = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
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
        code = st.selectbox("Select Class", getClassrooms())

        if code:
            clss =  getClassroom(code)
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
    if menu == "Change Student Class":
        st.header("Change Class or Promote Student")
        code = None
        code = st.selectbox("Class", getClassrooms())
        stud = None
        if code:
            fullNameId = getStudentsIdandNames(code)
            name = st.selectbox("Name", fullNameId.keys())

            if name:
                stud = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
        class_to_code = st.selectbox("Class To", [room for room in getClassrooms() if room != code])
        if class_to_code:
            clss_to = Class.query.filter_by(code=class_to_code).one()

            if st.button("Change Class") and stud and clss_to:
                stud.classroom_id = clss_to.id
                stud.save()
                st.dataframe(pd.DataFrame([stud.to_dict()]))
                st.success("Class changed successfully")

    if menu == "Update score":
        st.header("Update Scores")
        code = st.selectbox("Class", getClassrooms())
    
        if code:
            fullNameId = getStudentsIdandNames(code)
            name = st.selectbox("Name", fullNameId.keys())
            if name:
                stud = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
            if stud:
                subjectlist = [sub for sub in getclassSubjects(code) if sub in stud.subject_recoeded()]
                subjectname = st.selectbox("Subject", subjectlist)
        
                subject = Subject.query.filter_by(student_id=stud.id, name=subjectname).one_or_none()
                if subject:
                    ca = st.number_input("Continuous Assessment", 0, 30, subject.CA)    
                    exam = st.number_input("Third Term Score (Just the exam score)", 0, 70, subject.examScore)
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

    if menu == "Subject Recorded":
        st.header("Subject Recorded")
        code = st.selectbox("Class", getClassrooms())
    
        if code:
            clss =  getClassroom(code)
            students = clss.students
            subjectlist = [sub for sub in getclassSubjects(code)]
            subjectname = st.selectbox("Subject", subjectlist)
            studentlist = []
            for stud in students:
                obj = {}
                subject = Subject.query.filter_by(student_id=stud.id, name=subjectname).one_or_none()
                if subject:
                    obj["FULLNAME"] = stud.fullName
                    obj["CA"] = subject.CA
                    obj["EXAM SCORE"] = subject.examScore
                    obj["FIRST TERM SCORE"] = subject.firstTermScore
                    obj["SECOND TERM SCORE"] = subject.secondTermScore
                else:
                    obj["FULLNAME"] = stud.fullName
                studentlist.append(obj)

            st.dataframe(pd.DataFrame(studentlist))

    if menu == "Delete Students Score":
        st.header("Delete Students Record")
        code = st.selectbox("Class", getClassrooms())
    
        if code:
            clss =  getClassroom(code)
            students = clss.students
            if students:
                students.sort(key=lambda s: s.fullName)
            stdlist = [std.fullName for std in students]
            name = st.selectbox("Name", stdlist)
            fullNameId = getStudentsIdandNames(code)
            if name:
                stud = Student.query.filter(Student.id==fullNameId[name]).one_or_none()
            if stud:
                subjectlist = [sub for sub in getclassSubjects(code) if sub in stud.subject_recoeded()]
                subjectname = st.selectbox("Subject", subjectlist)
        
                subject = Subject.query.filter_by(student_id=stud.id, name=subjectname).one_or_none()
                st.dataframe(pd.DataFrame([subject.view_dict()]))
                if st.button("Delete") and subject:
                    subject.delete()
                    st.success("Record Deletes Successfully")

    if menu == "Upload CSV Record":
        csv_file = st.file_uploader("Upload CSV file", type="csv")
        csv_text = st.text_area("Past your csv text here")
        if csv_file:
            data = pd.read_csv(csv_file)
            st.dataframe(pd.DataFrame(data))

        if st.button("Upload") and csv_text:
            data = pd.read_csv(StringIO(csv_text))
            st.dataframe(pd.DataFrame(data))



        # arisekola77



viewStream()