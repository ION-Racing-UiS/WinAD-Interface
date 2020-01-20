from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, TextAreaField, FileField, SelectField, validators
from wtforms.fields.html5 import DateField

class RegisterForm(FlaskForm):
    department = SelectField(
        'Department',
        choices=[('chassis', 'Chassis'), ('electronics', 'Electronics'), ('it', 'IT'), ('management', 'Management'), ('marketing', 'Marketing'), ('powertrain', 'Powertrain'), ('suspension', 'Suspension')],
        validators=[],
        render_kw={'placeholder': 'Department'}
        )
    role = StringField(
        'Role',
        validators=[validators.DataRequired(message='Please input your role.'), validators.Length(min=2)],
        render_kw={'placeholder': 'Role or posistion'}
    )
    first_name = StringField(
        'First Name',
        validators=[validators.Length(min=2, max=32)],
        render_kw={'placeholder': 'First Name', 'oninput': 'setUsername()', 'onchange': 'setUsername()'},
        id='fname'
    )
    last_name = StringField(
        'Last Name',
        validators=[validators.Length(min=2, max=32)],
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