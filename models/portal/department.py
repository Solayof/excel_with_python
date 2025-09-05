#!/usr/bin/python3
"""department model
"""
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.baseModel import BaseModel
from models.portal.teacher import Teacher


class Department(BaseModel, Base):
    """department model

    Args:
        BaseModel (BaseModel class): Basemodel class
        Base (declarative class): declarative class
    """
    __tablename__ = "departments"
    extend_existing = True
    name = Column(String(36), nullable=False)
    hod_id = Column(String(64), ForeignKey("teachers._id", ondelete="SET NULL"))
    hod = relationship("Teacher", foreign_keys=[hod_id])
    teachers = relationship(
        "Teacher",
        foreign_keys='[Teacher.department_id]',
        back_populates="department",
        uselist=True
    )
    subjects = relationship(
        "Subject",
        foreign_keys="[Subject.department_id]",
        back_populates="department",
        uselist=True
    )
    
    students = relationship(
        "Student",
        foreign_keys='[Student.department_id]',
        back_populates="department",
        uselist=True
    )
    
    def save(self):
        if self.hod_id is not None:
            if Teacher.get(self.hod_d) not in self.teachers:
                raise ValueError(
                    f"Assigned HOD not a member of {self.name} department")
        return super().save()
