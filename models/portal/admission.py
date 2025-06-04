#!/usr/bin/python3
"""admission model
"""
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from models.portal.user import User


class Admission(User):
    """admission model

    Args:
        User (User): User class
    """    
    __tablename__ = "admission_register"
    extend_existing = True
    _id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    admission_no = Column(String(5), unique=True, nullable=False)
    
    
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
