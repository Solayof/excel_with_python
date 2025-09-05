from backup.portal.student import Student
from backup.portal.Class import Class
from backup.portal.subject import Subject


def getAllStudents():
    """get all students in the database

    Returns:
        list: list of student objects
    """    
    return Student.query.all()