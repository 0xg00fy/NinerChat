"""Create form logic."""
from wtforms import Form, StringField, PasswordField, validators, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo, Length, Optional, DataRequired
from application import college_majors
from application.models import Chatroom

def uncc_email_check(form,field):
        if not str(field.data).endswith('@uncc.edu'):
            raise ValidationError('Email must be an UNC Charlotte email')


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
            InputRequired(message=('Please enter a valid email address.')),
            uncc_email_check
        ])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(message='Please enter a password.'),
            Length(min=6, message=('Please select a stronger password.')),
            EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Old Password',)
    major = SelectField(
        "College Major",
        coerce=int,
        validators=[
            InputRequired()
        ])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # populate college major choices
        self.major.choices = college_majors.selection_list()


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
    confirm = PasswordField('Confirm Password',)
    major = SelectField(
        "College Major",
        coerce=int,
        validators=[
            InputRequired()
        ]
    )
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # populate college major choices
        self.major.choices = college_majors.selection_list()

class AddRoomForm(Form):
    """Add Room Form"""
    
    name = StringField(
        'Name',
        validators=[
            InputRequired(message=('Enter a fake name or something.'))
        ])
    public = SelectField(
        "Public/Private",
        coerce=int,
        choices=[(0,"Private"),(1,"Public"),],
        validators=[
            InputRequired()
        ]
    )

class SelectRoomForm(Form):
    """ Select Room Form"""
    room_id = SelectField(
        coerce=int,
        validators=[
            InputRequired()
        ]
    )
    submit = SubmitField('Add Room')

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        # populate room id choices
        rooms = Chatroom.query.all()
        room_list = [
                (room.id,room.name) for room in rooms
        ]
        self.room_id.label = 'Rooms'
        self.room_id.choices = room_list

class SelectPublicRoomForm(Form):
    """ Select Room Form"""
    room_id = SelectField(
        coerce=int,
        validators=[
            InputRequired()
        ]
    )
    submit = SubmitField('Add Room')

    def __init__(self, filter=None, *args, **kwargs):
        super().__init__(*args,**kwargs)
        # populate room id choices
        rooms = Chatroom.query.filter_by(public=True).all()
        room_list = [
                (room.id,room.name) for room in rooms
        ]
        self.room_id.label = 'Public Rooms'
        self.room_id.choices = room_list

class SelectPrivateRoomForm(Form):
    """ Select Room Form"""
    room_id = SelectField(
        coerce=int,
        validators=[
            InputRequired()
        ]
    )
    submit = SubmitField('Add Room')

    def __init__(self, filter=None, *args, **kwargs):
        super().__init__(*args,**kwargs)
        # populate room id choices
        rooms = Chatroom.query.filter_by(public=False).all()
        room_list = [
                (room.id,room.name) for room in rooms
        ]
        self.room_id.label = 'Private Rooms'
        self.room_id.choices = room_list

class ChatPostForm(Form):
    """Chat Post Form"""
    
    text = TextAreaField(
        '',
        validators=[
            InputRequired(message=('Please enter something to post'))
        ])
