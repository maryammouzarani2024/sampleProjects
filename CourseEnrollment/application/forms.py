from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User

class LoginForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=StringField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    remember_me=BooleanField("Remember Me")
    submit=SubmitField("login")

class CourseAddForm(FlaskForm):
    title=StringField("title", validators=[DataRequired(), Length(min=3, max=15)])
    description=StringField("description", validators=[DataRequired()])
    credits=IntegerField("credits", validators=[DataRequired()])
    term=StringField("term", validators=[DataRequired()])
    submit=SubmitField("add")

class RegistrationForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=StringField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    password_confirm=StringField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    first_name=StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    last_name=StringField("Last Name",validators=[DataRequired(),Length(min=2, max=50)])
    submit=SubmitField("Register")

    def validate_email(self, email):
        user=User.objects(email=email.data).first()# find the first user in the user model with the same email
        if user:
            raise ValidationError("Email is already in use. Pick another one.")