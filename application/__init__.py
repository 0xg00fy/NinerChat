from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_object):
    app = Flask(__name__, instance_relative_config=False)

    # Application configuration
    app.config.from_object(config_object)

    # Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # import parts of app
        from . import auth, routes, profile, room

        # import API
        from application.api import auth as api_auth
        from application.api import profile as api_profile
        from application.api import room as api_room

        # register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(profile.profile_bp)
        app.register_blueprint(room.room_bp)
        app.register_blueprint(api.api_bp)

        db.create_all()

        # add admin user if none exists
        from application.models import User
        if User.query.filter_by(email='ninerchat@uncc.edu').first() is None:
            admin_user = User(
                username='admin',
                email='ninerchat@uncc.edu',
                password='admin',
                admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
        
        # add building chatrooms
        from application.room import add_room
        for room in BUILDINGS:
            add_room(room,public=True)

        return app

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
    ],
    'None':[
        'Undecided',
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

class CollegeMajors:
    """ 
    Stores the college majors as an object and returns the list of
    majors as lists and dictionaries to be used in menus and drop down lists
    """
    def __init__(self):
        from . import UNDERGRAD_MAJORS as majors
        majors_list = [
            (clg,mjr) for clg in majors.keys() for mjr in majors[clg]
        ]
        index = range(len(majors_list))
        self.majors_dict = {
            n:item for (n,item) in zip(index,majors_list)
        }
        self.majors_text = [
            '{} : {}'.format(clg,mjr) for (clg,mjr) in majors_list
        ]
        self.majors_select = [
            (value,label) for value,label in zip(self.majors_dict.keys(),self.majors_text)
        ]
    def selection_list(self):
        return self.majors_select
    
    def get(self,id):
        index = int(id)
        return self.majors_dict.get(index)
    
    def get_college(self,id):
        index = int(id)
        return self.majors_dict.get(index)[0]
    
    def get_major(self,id):
        index = int(id)
        return self.majors_dict.get(index)[1]

college_majors = CollegeMajors()