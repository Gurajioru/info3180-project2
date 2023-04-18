# Add any form classes for Flask-WTF here
# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    firstname = StringField('FirstName', validators=[InputRequired()])
    lastname = StringField('LastName', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    biography=TextAreaField('Description',validators=[InputRequired()])
    profile_pic= FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
