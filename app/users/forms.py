from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired,Email,Length

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators = [ DataRequired(), Email(), Length(min = 6, max = 120)])
    password = StringField('Password', validators = [ DataRequired(), Length(min = 8)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [ DataRequired(), Email(), Length(min = 6, max = 120)])
    password = StringField('Password', validators = [DataRequired(), Length(min = 8)])
    submit = SubmitField('Login')

class EmailForm(FlaskForm):
    email = StringField('Email', validators = [ DataRequired(), Email(), Length(min = 6, max = 120)])
    submit = SubmitField('Submit')

class PasswordResetForm(FlaskForm):
    password = StringField('New Password', validators = [DataRequired(), Length(min = 8)])
    retype_password = StringField('Repeat Password', validators = [DataRequired(), Length(min = 8)])
    submit = SubmitField('Reset Password')

class ChangePasswordForm(FlaskForm):
    current_password = StringField('Current Password', validators = [DataRequired(), Length(min = 8)])
    new_password = StringField('New Password', validators = [DataRequired(), Length(min = 8)])
    submit = SubmitField('Change Password')