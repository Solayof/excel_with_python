#!/usr/bin/python3
"""user models"""
from datetime import date, datetime
from sqlalchemy import Column, DateTime, Integer, String
from uuid import uuid4
import models
from models.baseModel import BaseModel



class UserModel(BaseModel):
    """user base model

    Args:
        BaseModel (_type_): General basemodel

    Returns:
        _type_: None
    """    
    def __init__(self, *args, **kwargs):
        """initializing user basemodel
        """
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """        
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
        new_dict.pop("_password", None)
        if "dob" in new_dict and new_dict["dob"] is not None:
            new_dict["dob"] = new_dict["dob"].strftime("%Y-%m-%d")
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        return new_dict

    def get_id(self):
        """get user id to login

        Returns:
            _type_: string
        """ 
        return self.id

    @property
    def fullName(self):
        """object instance fullname

        Returns:
            _type_: string
        """        
        return f"{self.lastName} {self.middleName} {self.firstName}"
    
    def __repr__(self):
        """string representation

        Returns:
            _type_: string
        """
        rep = {
          self.id: self.fullName
        }
        return f"{rep}"

