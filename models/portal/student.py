#!/usr/bin/python3
"""student model
"""
from sqlalchemy import Column, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from models.portal.cache import current_session, current_term
from models.portal.admission import Admission
from models.portal.subject import Subject



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

    def subjects_to_dict(self, term=None, session=None):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """
        if not session:
            session = current_session()
        if term:     
            subjects = self.term_subject(term=term, session=session)
        else:
            subjects = self.subjects

        new_dict ={sub.name : sub.view_dict() for sub in subjects}
        
                
        return new_dict
    
    def subject_recorded(self, term=None, session=None):
        subjects = self.term_subject(term=term, session=session)

        return [sub.name for sub in subjects]

    def term_subject(self, term=None, session=None):
        if not session:
            session = current_session()
        if not term:
            term = current_term()
        return Subject.query.filter_by(student_id=self.id, term=term, session=session).all()
    
    def subjects_sessions(self, term=None):
        if not term:
            term = current_term()
        subjects = Subject.query.with_entities(Subject.session).filter_by(student_id=self.id, term=term).distinct().all()
        return [sub[0] for sub in subjects if sub[0]]
    
    def subjects_scores(self, term=None, session=None):
        if not session:
            session = current_session()
        if term:     
            subjects = self.term_subject(term=term, session=session)
        else:
            subjects = self.subjects

        return [sub.view_dict() for sub in subjects]
    
    def overall_subjects_scores(self):
        subjects_dict = {}
        for sub in self.classroom.sheetSubjects:
            sub_dict = {}
            term_subject = Subject.query.filter_by(
                student_id=self.id, name=sub, term=current_term()).one_or_none()
            if term_subject:
                sub_dict = term_subject.view_dict()
            
            subjects = Subject.query.filter_by(student_id=self.id, name=sub).all()
            if subjects:
                    sub_dict.update({s.term: s.totalScore for s in subjects if s.term != current_term()})
            subjects_dict.update({sub: sub_dict})
        return subjects_dict  

            
