import jwt
import datetime as dt
import json
from flask import current_app as app
from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash
from .models import db, User

jwt_algorithm = 'HS256'
secret_key = app.config.get('SECRET_KEY')

class TestToken:
    """ A token used during testing

    TestToken replaces token generation by jwt due to
    the library not working in a testing framework.
    """
    def __init__(self,id):
        self.token = id
        self.sub = id
    
    def decode(self):
        """ replaces decode method in jwt tokens """
        return self.token # returns user id

def encode_token(user_id):
    """ Generates token for authorization"""

    # Generates testing token
    if app.config.get('TESTING') == True:
        return TestToken(user_id)
    
    payload = {
        'exp': dt.datetime.utcnow() + dt.timedelta(seconds=5),
        'iat': dt.datetime.utcnow(),
        'sub': user_id
    }

    # Returns auth token containing user id
    return jwt.encode(
        payload,
        secret_key,
        jwt_algorithm
    )

def decode_token(token):
    """Returns contents of token"""

    # Decodes testing token
    if app.config.get('TESTING') == True:
        return token.sub
    
    try:
        payload = jwt.decode(
            token,
            secret_key
        )
        # Returns decoded user id in token
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Expired Signature'
    except jwt.InvalidTokenError:
        return 'Invalid Token'

# Blueprint Configuration
api_bp = Blueprint('api_bp', __name__,
    url_prefix='/api',
    template_folder='templates',
    static_folder='static')

@api_bp.route('/signup', methods=['POST'])
def signup():
    """User sign-up using API"""
    
    # Get posted JSON data
    signup_data = request.get_json()
    name = signup_data['name']
    email = signup_data['email']
    password = signup_data['password']
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is None:
        # Create and add user to database
        user = User(username=name,
                    email=email,
                    password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        
        # generate auth token
        token = encode_token(user.id)
        
        # Respond with success message and token
        response = {
            'status': 'success',
            'message': 'successfully registered.',
            'token': token.decode()
        }
        return make_response(jsonify(response)), 201
    
    # failure user exists or invalid info
    else:
        response = {
            'status': 'failure',
            'message': 'could not be registered.',
        }
        return make_response(jsonify(response)), 400

@api_bp.route('/login', methods=['POST'])
def login():
    """User login using API"""
    
    # Get posted JSON data
    login_data = request.get_json()
    email = login_data['email']
    password = login_data['password']

    # Find user by email
    user = User.query.filter_by(email=email).first()
    if user:
        # Check password
        if user.check_password(password=password):
            token = encode_token(user.id)
            response = {
                'status': 'success',
                'message': 'sucessfully logged in.',
                'token': token.decode()
            }
            return make_response(jsonify(response)), 200
    
    # Failure email or password is incorrect
    response = {
        'status': 'failure',
        'message': 'email or password incorrect.',
    }
    return make_response(jsonify(response)), 401

@api_bp.route('/profile', methods=['POST'])
def profile():
    """ Access profile information using API"""

    # Get posted JSON data
    auth_data = request.get_json()
    
    # get token and decode to get user id
    auth_token = auth_data['token']
    user_id = decode_token(auth_token)

    # check if token valid
    if user_id == 'Invalid Token':
        response = {
            'status': 'failure',
            'message': 'invalid token.'
        }
        return make_response(jsonify(response)), 400
    # check if token expired
    if user_id == 'Expired Signature':
        response = {
            'status': 'failure',
            'message': 'expired signature.'
        }
        return make_response(jsonify(response)), 400
    
    
    # get user from database
    user = User.query.filter_by(id=user_id).first()
    if user:
        response = {
            'status': 'success',
            'message': 'profile found.',
            'name': user.username,
            'email': user.email
        }

        return make_response(jsonify(response)), 200

    # user does not exist
    else:
        response = {
            'status': 'failure',
            'message': 'profile not found,'
        }

        return make_response(jsonify(response)), 404
