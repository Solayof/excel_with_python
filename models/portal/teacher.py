#!/usr/bin/python3
"""teacher class
"""
from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from models.portal.user import User
from models.portal.Class import Class


class Teacher(User):
    """teacher model

    Args:
        User (_type_): user class
    """    
    __tablename__ = "teachers"
    extend_existing = True
    _id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    staff_id = Column(String(16))
    file_no = Column(String(16))
    grade_level = Column(String(4))
    previous_school = Column(String(64))
    date_transfer = Column(Date)
    last_promote_date = Column(Date)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"))
    department = relationship(
        "Department",
        foreign_keys=[department_id],
        back_populates="teachers",
        uselist=False
    )

    def to_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """ 
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
        new_dict.pop("_password", None)
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["dob"] = self.dob.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        new_dict['isAdmin'] = self.isAdmin()
        new_dict['userType'] = "teachers"
        
        formclass = self.formClass
        new_dict["formclass_id"] = formclass.id if formclass else None
                
        courses = self.course_teach
        new_dict["number_of_courses"] = len(courses) if courses else 0
        
        return new_dict

    def course_teach_paginate(self, page=1, per_page=10):
        if per_page == 0  or page == 0:
            return None
        offset = (page - 1) * per_page
        length = len(self.course_teach)
        if offset >= length:
            return None
        remain = length - offset
        end = offset + per_page if remain >= per_page else offset + remain
        nxt_page = page + 1 if page * per_page < length else 1
        courses = {
            
              "page": page,
              "total": len(self.course_teach),
              "next_page": nxt_page
            ,

            "courses": [{
            self.course_teach[i].to_dict()
            } for i in  range(offset, end)]
        }
        return courses
