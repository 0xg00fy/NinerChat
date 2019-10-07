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
    def __init__(self,id):
        self.token = '00.00.TestToken'
        self.sub = id

    
    def decode(self):
        return self.token

def encode_token(user_id):
    """ Generates token for authorization"""

    # Generates Testing Token
    if app.config.get('TESTING') == True:
        return TestToken(user_id)
    
    payload = {
        'exp': dt.datetime.utcnow() + dt.timedelta(seconds=5),
        'iat': dt.datetime.utcnow(),
        'sub': user_id
    }

    return jwt.encode(
        payload,
        secret_key,
        jwt_algorithm
    )

def decode_token(token):
    """Returns contents of token"""
    if app.config.get('TESTING') == True:
        return token.sub
    try:
        payload = jwt.decode(
            token,
            secret_key
        )
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
    signup_data = request.get_json()
    name = signup_data['name']
    email = signup_data['email']
    password = signup_data['password']
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is None:
        user = User(username=name,
                    email=email,
                    password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        token = encode_token(user.id)
        response = {
            'status': 'success',
            'message': 'successfully registered.',
            'token': token.decode()
        }
        return make_response(jsonify(response)), 201
    else:
        response = {
            'status': 'failure',
            'message': 'could not be registered.',
        }
        return make_response(jsonify(response)), 400

@api_bp.route('/login', methods=['POST'])
def login():
    """User login using API"""
    login_data = request.get_json()
    email = login_data['email']
    password = login_data['password']
    user = User.query.filter_by(email=email).first()
    if user:
        if user.check_password(password=password):
            token = encode_token(user.id)
            response = {
                'status': 'success',
                'message': 'sucessfully logged in.',
                'token': token.decode()
            }
            return make_response(jsonify(response)), 200
    response = {
        'status': 'failure',
        'message': 'email or password incorrect.',
    }
    return make_response(jsonify(response)), 401
