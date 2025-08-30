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
                          session_list, grade)
from models.portal.admission import Admission
from models.portal.cache import current_session, current_term, term_list
from models.portal.Class import Class

from models.portal.student import Student
from models.portal.subject import Subject

from models.portal.user import User

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
st.title("Class Performance analytics")


def class_performance():
    st.header("📈 Performance Analytics")
    code = st.selectbox("Select Class", getClassrooms())

    if code:
        clss =  getClassroom(code)
        students = Student.query.filter_by(classroom_id=clss.id).all()

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
                        "Total Score": total_score,
                        "Number of Subject Recorded": len(scores),
                        "Average Score": avg_score,
                    })

            if performance_data:
                df_perf = pd.DataFrame(performance_data).sort_values(by="Average Score", ascending=False)

                # Grade Distribution
                
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

class_performance()
