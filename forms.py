from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, \
    BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
from models import User


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField()
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('pass_confirm', message='Passwords Must Match!')
    ])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


class UploadFile(FlaskForm):
    json = FileField('Logo', validators=[FileRequired()])
    submit = SubmitField('Upload')
