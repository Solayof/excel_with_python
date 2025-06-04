#!/usr/bin/python3
"""class model
"""
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.utils import coordinate_to_tuple, get_column_letter
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.engine.dbSheet import Workbook
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

            yr = int(datetime.now().strftime("%y"))
            mth = datetime.now().strftime("%m")
            if int(mth) < 8:
                yr = yr - 1
            kwargs["code"] = code + "-" + f"20{yr}-20{yr + 1}"
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
    
    def getSheet(self):
        filePath = f"{self.className[:3]}.xlsx"
        worksheet = Workbook(filePath=filePath)
        worksheet.open_session()

        return worksheet
    
    def generateSheet(self):
        students = self.students
        worksheet = self.getSheet()
        worksheet.open_session()

        stdcell = "b4"
        for student in students:
            worksheet.writeCell(cell=stdcell, value=student.fullName)
            subjects = student.subjects
            stdrow, stdcol = coordinate_to_tuple(stdcell)
            admnocell = f"{get_column_letter(stdcol + 1)}{stdrow}"
            worksheet.writeCell(cell=admnocell, value=student.admission_no)
            gendercell = f"{get_column_letter(stdcol + 2)}{stdrow}"
            worksheet.writeCell(cell=gendercell, value=student.gender)
            classcell = f"{get_column_letter(stdcol + 3)}{stdrow}"
            worksheet.writeCell(cell=classcell, value=student.classroom.className)
            for subject in subjects:
                subCell = worksheet.getSubjectCell(subject=subject.name)
                _, subcol = coordinate_to_tuple(subCell)

                CAcell = f"{get_column_letter(subcol)}{stdrow}"
                worksheet.writeCell(cell=CAcell, value=subject.CA)
                examcell = f"{get_column_letter(subcol + 1)}{stdrow}"
                worksheet.writeCell(cell=examcell, value=subject.examScore)
                scdtermcell = f"{get_column_letter(subcol + 3)}{stdrow}"
                worksheet.writeCell(cell=scdtermcell, value=subject.secondTermScore)
                frttermcell = f"{get_column_letter(subcol + 4)}{stdrow}"
                worksheet.writeCell(cell=frttermcell, value=subject.firstTermScore)
                


            stdcell = f"{get_column_letter(stdcol)}{stdrow + 1}"

        worksheet.saveWorkbook(self.code)

    @property
    def sheetSubjects(self):
        return self.getSheet().dbSubjects()


