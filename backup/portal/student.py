#!/usr/bin/python3
"""student model
"""
from sqlalchemy import Column, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from backup.portal.admission import Admission


class Student(Admission):
    """student model
    
    Usage: student = Student(
            username="jesa",
            email="asd@gdha",
            admission_no="231",
            arm="A"
        )
        other parameters are optional

    Args:
        Admission (_type_): admission class
    """    
    __tablename__ = "students"
    extend_existing = True
    _id = Column(
        String(36),
        ForeignKey('admission_register._id'),
        primary_key=True
        )
    classroom_id = Column(String(36), ForeignKey("classes.id"))
    classroom = relationship(
        "Class",
        foreign_keys=[classroom_id],
        back_populates="students",
        uselist=False
        )
    subjects = relationship("Subject",
        foreign_keys="[Subject.student_id]",
        back_populates="student",
        uselist=True)
    

    def to_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """        
        new_dict = {}
        new_dict["FullName"] = self.fullName
        
        new_dict["Gender"] = self.gender

        new_dict["Admission Number"] = self.admission_no
        
        
        classroom = self.classroom
        new_dict["classroom"] = classroom.className if classroom else None
        
                
        return new_dict

    def subjects_to_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """        
        subjects = self.subjects

        new_dict ={sub.name : sub.view_dict() for sub in subjects}
        
                
        return new_dict
    
    def subject_recoeded(self):
        subjects = self.subjects

        return [sub.name for sub in subjects]

