from application import db
from werkzeug.security import generate_password_hash, check_password_hash 


class User(db.Document):
    user_id=db.IntField(unique=True)
    first_name=db.StringField(max_length=50)
    last_name=db.StringField(max_length=50)
    email=db.StringField(max_length=50, unique=True)
    password=db.StringField()

    def set_password(self, password):
        self.password=generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Course(db.Document):
    courseID=db.IntField(unique=True)
    title=db.StringField(max_length=30)
    description=db.StringField(max_length=100)
    credits=db.IntField()
    term=db.StringField(max_length=30)

class Enrollment(db.Document):
    user_id=db.IntField()
    course_id=db.StringField(max_length=10)


