from backup.portal.student import Student
from backup.portal.Class import Class
from backup.portal.subject import Subject


def get_classes():
    return Class.query.all()