#!/usr/bin/python3
"""admin model
"""
from sqlalchemy import Column, ForeignKey, JSON, String
from models.base import Base
from models.baseModel import BaseModel
from models.customExcept import InvalidAdmin
from models.portal.teacher import Teacher


class Admin(BaseModel, Base):
    """admin model

    Args:
        Teacher (_type_): Teacher model class
    """
    __tablename__ = "admins"
    extend_existing = True
    teacher_id = Column(
        String(36),
        ForeignKey("teachers._id", ondelete="CASCADE"),
        nullable=False
        )
    privileges = Column(JSON())
    
    def __init__(self, *args, **kwargs):
        """initialize admin model

        Raises:
            InvalidUser: customize User exception
        """
        self.privileges = {
            "create": False,
            "delete": False,
            "update": False,
            "superadmin": False
        }
        if Teacher.get(kwargs["teacher_id"]) is None:
            raise InvalidAdmin("User not valid")
        super().__init__(*args, **kwargs)
 
    def save(self):
        """admin save method

        Raises:
            InvalidUser: customize User exception
        """   
        if Teacher.get(self.teacher_id) is None:
            raise InvalidAdmin("User not valid")
        adm = self.get(self.id)
        # check to ensure no admin teacher id is change
        if adm is not None:
            if adm.teacher_id != self.teacher_id:
                raise InvalidAdmin("teacher id can't be changed")
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
        new_dict["fullName"] = Teacher.get(self.teacher_id).fullName
        return new_dict
