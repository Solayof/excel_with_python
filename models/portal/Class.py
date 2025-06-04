#!/usr/bin/python3
"""class model
"""
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.baseModel import BaseModel

class Class(BaseModel, Base):
    """class model
    
    Usage: jss1 = Class(className="Jss 1")
            others parameters are optional

    Args:
        BaseModel (_type_): Basemodel class
        Base (_type_): declarative base
    """    
    __tablename__ = "classes"
    extend_existing = True
    code = Column(String(16), unique=True)
    arm = Column(String(1))
    session = Column(String(9))
    className = Column(String(6)) 
    students = relationship(
        "Student",
        foreign_keys="[Student.classroom_id]",
        back_populates="classroom",
        uselist=True
        )

    def __init__(self, *args, **kwargs):
        """initializing class
        """        
        if kwargs:
            className = kwargs.pop("className", None)
            arm = kwargs.pop("arm", None)

        if className:
            className = className.upper() + arm.upper()
            code = className.replace(" ", "-")

            yr = datetime.now().strftime("%y")
            kwargs["code"] = code + "-" + f"20{yr}-20{int(yr) + 1}"
            kwargs["className"] = className
            kwargs["arm"] = arm
            super().__init__(*args, **kwargs)

    def save(self):
        """class save method
        """        
        if not self.session:
            yr = datetime.now().strftime("%y")
            self.session = f"20{yr}-20{int(yr) + 1}"
        super().save()
        
    def to_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """        
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
       
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        
        students = self.students
        new_dict["number_of_students"] = len(students) if students else 0
        
        
        
        return new_dict
