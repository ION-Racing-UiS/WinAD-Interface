from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, TextAreaField, FileField, SelectField, validators
from wtforms.fields.html5 import DateField
import app.pylib.win_user
import re

reg_ex = app.pylib.win_user.ou_regex
# Regex for different OUs

class RegisterForm(FlaskForm):
    department = SelectField(
        'Department',
        choices=app.pylib.win_user.ous,
        validators=[],
        render_kw={'placeholder': 'Department'}
        )
    role = StringField(
        'Role',
        validators=[validators.DataRequired(message='Please input your role.'), validators.Length(min=2), validators.Regexp(regex=reg_ex, flags=re.IGNORECASE, message="Role cannot be equal to a department name.")],
        render_kw={'placeholder': 'Role or posistion'}
    )
    first_name = StringField(
        'First Name',
        validators=[validators.Length(min=2, max=32), validators.Regexp(regex=reg_ex, message="First name cannot be equal to a department name.")],
        render_kw={'placeholder': 'First Name', 'oninput': 'setUsername()', 'onchange': 'setUsername()'},
        id='fname'
    )
    last_name = StringField(
        'Last Name',
        validators=[validators.Length(min=2, max=32), validators.Regexp(regex=reg_ex, message="Last name cannot be equal to a department name.")],
        render_kw={'placeholder': 'Last Name', 'oninput': 'setUsername()', 'onchange': 'setUsername()'},
        id='lname'
    )
    full_name = StringField(
        'Full Name',
        render_kw={'placeholder': 'We\'ll take care of this one', 'readonly': True},
        id='fullname'
    )
    user_name = StringField(
        'Username',
        render_kw={'placeholder': 'Created by username policy', 'readonly': True},
        id='username'
    )
    email = StringField(
        'Email',
        validators=[validators.Email(message='Please enter your email.'), validators.Length(min=6, max=128)],
        render_kw={'placeholder': 'Email'}
    )
    password = PasswordField(
        'Password',
        validators=[validators.DataRequired(message="Please enter a password"), validators.Length(min=3)],
        render_kw={'placeholder': 'Password'}
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[validators.EqualTo('password', message='Passwords must match!')],
        render_kw={'placeholder': 'Confirm Password'}
    )
    terms = BooleanField(
        'Terms',
        validators=[validators.DataRequired('You must agree to the terms and conditions')]
    )
    submit = SubmitField('Register User', render_kw={'class': 'btn email-me'})