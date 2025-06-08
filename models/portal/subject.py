#!/usr/bin/python3
"""subject model
"""
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from models.base import Base
from models.baseModel import BaseModel


class Subject(BaseModel, Base):
    """subject model
    
    Usage: mathematics = Subject(
        name="Mathematics"
        code="MTH"
        )
        ohter parameters are optional

    Args:
        BaseModel (_type_): basemodel class
        Base (_type_): declarative base
    """
    __tablename__ = "subjects"
    extend_existing = True
    name = Column(String(20), nullable=False, unique=True)
    CA = Column(Integer())
    examScore = Column(Integer())
    firstTermScore = Column(Integer())
    secondTermScore = Column(Integer())
    student_id = Column(String(36), ForeignKey("students._id"))
    student = relationship("Student",
        foreign_keys=[student_id],
        back_populates="subjects",
        uselist=False)
    
    
    
    
    def to_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """        
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
        new_dict.pop("_password", None)
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        
        
        return new_dict

    def view_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """        
        new_dict = {}

        new_dict["CA"] = self.CA
        new_dict["Exam"] = self.examScore
        new_dict["Second Term Score"] = self.secondTermScore
        new_dict["First Term Score"] = self.firstTermScore
        
        
        return new_dict
    

    @classmethod
    def all(cls):
        objs = {}
        return objs


