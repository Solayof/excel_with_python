#!/usr/bin/python3
"""user model
"""
from datetime import datetime, timezone
from hashlib import sha256
from sqlalchemy import Column, DateTime, String
from backup.base import Base
from backup.portal.usermodel import UserModel
import backup


class User(UserModel, Base):
    """user model definition

    Args:
        UserModel (_type_): user basemodel
        Base (_type_): Declarative base
        UserMixin (_type_): flask usermixin
    """
    __tablename__ = "users"
    firstName = Column(String(36))
    middleName = Column(String(36))
    lastName = Column(String(36))
    gender = Column(String(6))
   
    
    @classmethod
    def all(cls):
        """get all the instances of the class in dict

        Returns:
            bool: dict of all the class instances
        """        
        objs = {}
        for obj in cls.query.all():
            objs[obj.username] = obj.to_dict()
        return objs

