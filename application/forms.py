"""Create form logic."""
from wtforms import Form, StringField, PasswordField, validators, SubmitField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo, Length, Optional


class SignupForm(Form):
    """User Signup Form."""
    name = StringField(
        'Name',
        validators=[
            InputRequired(message=('Enter a fake name or something.'))
        ])
    email = StringField(
        'Email',
        validators=[
            Length(min=6, message=('Please enter a valid email address.')),
            Email(message=('Please enter a valid email address.')),
            InputRequired(message=('Please enter a valid email address.'))
        ])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(message='Please enter a password.'),
            Length(min=6, message=('Please select a stronger password.')),
            EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Confirm Your Password',)
    submit = SubmitField('Register')


class LoginForm(Form):
    """User Login Form."""
    email = StringField(
        'Email',
        validators=[
            InputRequired('Please enter a valid email address.'),
            Email('Please enter a valid email address.')
        ])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired('Uhh, your password tho?')
        ])
    submit = SubmitField('Log In')

class ProfileForm(Form):
    """User Profile Form."""
    name = StringField(
        'Name',
        validators=[
            InputRequired(message=('Enter a fake name or something.'))
        ])
    oldpassword = PasswordField(
        'Old Password',
        validators=[
            InputRequired(message='Please enter a password.'),
            Length(min=6, message=('Please select a stronger password.')),
        ])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(message='Please enter a password.'),
            Length(min=6, message=('Please select a stronger password.')),
            EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Confirm Your Password',)
    submit = SubmitField('Register')

class AddRoomForm(Form):
    """Add Room Form"""
    name = StringField(
        'Name',
        validators=[
            InputRequired(message=('Enter a fake name or something.'))
        ])
