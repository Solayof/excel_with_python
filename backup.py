# print(Student.query.count())
from backup.getclass import get_classes
from backup.student_readers import getAllStudents
from models.portal.Class import Class
from models.portal.department import Department
from models.portal.student import Student

depart = Department()
depart.name = "GENERAL"
depart.save()


for clss in get_classes():
    new_class = Class()
    new_class.arm = clss.arm
    new_class.id = clss.id
    new_class.className = clss.className
    new_class.code = clss.code
    new_class.session = clss.session
    new_class.department_id = depart.id
    new_class.save()

for stud in getAllStudents():
    student = Student()
    student.firstName = stud.firstName
    student.lastName = stud.lastName
    student.middleName = stud.middleName
    student.admission_no = stud.admission_no
    student.classroom_id = stud.classroom_id
    student.gender = stud.gender
    student.username = stud.admission_no
    student.email = stud.admission_no
    student.password = stud.admission_no
    student.save()
 