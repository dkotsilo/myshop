from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError
from wtforms import TextField, SubmitField

from flask_wtf import FlaskForm, Form
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField  

#email = EmailField("Email", [InputRequired("Please enter your email address."), Email("Please enter your email address.")])
class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=55)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])