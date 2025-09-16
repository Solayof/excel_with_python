from models.portal.admin import Admin
from models.portal.teacher import Teacher
from models.portal.student import Student
from models.portal.Class import Class
from models.portal.department import Department
from models.portal.subject import Subject


teacher = Teacher()
teacher.lastName = "MOSES"
teacher.firstName = "SOLOMON"
teacher.middleName = "AYOFEMI"
teacher.username = "solayof"
teacher.email = "solomonayofemi@gmail.com"
teacher.password = "solayof"
teacher.save()
admin = Admin(teacher_id=teacher.id)

admin.privileges = {
            "create": True,
            "delete": True,
            "update": True,
            "superadmin": True
        }
admin.save()

# for k, v in info.items():
#         if v.lower() == "false":
#             v = False
#         elif v.lower() == "true":
#             v = True
#         else:
#             return jsonify({"error": "not bool"})
#         # Ensure the right kind of privileges are set and 
#         # of boolean type
#         if k in authKey and isinstance(v, bool):
#             admin.privileges[k] = v
#     # Ensure SQLAlchemy detect the change in privileges
#     flag_modified(admin, "privileges")
#     # commit the change to database
#     admin.save()