from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True)
    username = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False)
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False)
    password = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False)
    admin = db.Column(
        db.Boolean(),
        default=False
    )
    major = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False)

    def __init__(self, username, email, password, 
        admin=False, major='Undecided'):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.admin = admin
        self.major = major

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Chatroom(db.Model):
    """Model for Chat Rooms"""
    __tablename__ = 'chatrooms'
    id = db.Column(
        db.Integer,
        primary_key=True)
    name = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False)

    def __repr__(self):
        return '<Chatroom %r>' % self.name

class MemberList(db.Model):
    """Model for Chatroom MemberLists"""
    __tablename__ = 'member_list'
    id = db.Column(
        db.Integer,
        primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        unique=False)
    chatroom_id = db.Column(
        db.Integer,
        db.ForeignKey('chatrooms.id'),
        nullable=False,
        unique=False)

    user = db.relationship('User', backref='member_list')
    chatroom = db.relationship('Chatroom', backref='member_list')

    def __repr__(self):
        return '<MemberList %r-%r>' % (self.chatroom.name,self.user.username)

class Blacklist(db.Model):
    """Model for user blacklists"""
    __tablename__ = 'blacklist'
    id = db.Column(
        db.Integer,
        primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        unique=True)
    reason = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False)

    user = db.relationship('User', backref='blacklist')

    def __repr__(self):
        return '<Blacklist %r>' % self.user.username

class Messages(db.Model):
    """Model for chatroom messages"""
    __tablename__='messages'
    id = db.Column(
        db.Integer,
        primary_key=True)
    ts = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)
    chatroom_id = db.Column(
        db.Integer,
        db.ForeignKey('chatrooms.id'),
        nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    text = db.Column(
        db.Text,
        nullable=False)

    chatroom = db.relationship('Chatroom', backref='messages')
    user = db.relationship('User', backref='messages')

    def __repr__(self):
        return '<Messages %r>' % self.id

## Dictionary for Undergraduate Majors
## Used to generate a list of majors for users to choose from.
## Could be moved to a different location or read from CSV file in the future
UNDERGRAD_MAJORS = {
    'Arts and Architecture':[
        'Architecture','Art','Dance','Music','Theatre'
    ],
    'Business':[
        'Accounting','Business Analytics','Economics','Finance',
        'International Business','Management','Management Information Systems',
        'Marketing','Operations and Supply Chain Management'
    ],
    'Computing and Informatics':[
        'Computer Science',
    ],
    'Education':[
        'Child and Family Development','Elementary Education','Middle Grades',
        'Education','Special Education'
    ],
    'Engineering':[
        'Civil Engineering','Computer Engineering','Construction Management',
        'Electrical Engineering','Fire and Safety Engineering Technology',
        'Mechanical Engineering','Mechanical Engineering Technology',
        'Systems Engineering'
    ],
    'Health and Human Services':[
        'Exercise Science','Health Systems Management',
        'Neurodiagnostics and Sleep Science','Nursing','Public Health',
        'Respiratory Therapy','Social Work'
    ],
    'Liberal Arts and Sciences':[
        'Africana Studies','Anthropology','Biology','Chemistry',
        'Communication Studies','Criminal Justice',
        'Earth and Environmental Sciences','English','Environmental Studies',
        'French','Geography','Geology','German','History',
        'International Studies','Japanese Studies','Latin American Studies',
        'Mathematics','Mathematics for Business','Meteorology','Philosophy',
        'Physics','Political Science','Psychology','Religious Studies',
        'Sociology','Spanish'
    ]
}

## Dictionary of UNC Charlotte Buildings
## Used to generate building specific chatrooms
BUILDINGS = [
    'Atkins','Barnhardt','Bioinformatic','Barnard','Burson','Cameron',
    'College of Education','College of Health and Human Services','Colvard',
    'Cone Center', 'Cypress','Denny','Duke Centennial','EPIC','Fretwell',
    'Friday','Garinger','Grigg','Hawthorne','Student Health',
    'Johnson Band Center','Kennedy','Macy','McEniry','McMillan Greenhouse',
    'Memorial','Robinson', 'Rowe','Smith','Storrs','Student Union','Winningham',
    'Witherspoon','Woodward'
]