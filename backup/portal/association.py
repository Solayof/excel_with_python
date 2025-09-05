#!/usr/bin/python3

from sqlalchemy import Column, ForeignKey, String, Table
from models.base import Base



# student_courses_asso = Table("students_subjects",
#     Base.metadata,
#     Column("student_id", String(36), ForeignKey("students._id")),
#     Column("course_id", String(36), ForeignKey("courses.id"))
# )

