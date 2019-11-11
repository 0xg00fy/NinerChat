import jwt
import datetime as dt
import json
from flask import current_app as app
from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash
from .models import db, User, Chatroom, MemberList, Messages

jwt_algorithm = 'HS256'
secret_key = app.config.get('SECRET_KEY')

class TokenPayload:
    """TokenPayload object used by decode_token"""
    def __init__(self,valid,value):
        self.valid = valid
        self.value = value


class TestToken:
    """ A token used during testing

    TestToken replaces token generation by jwt due to
    the library not working in a testing framework.
    """
    def __init__(self,id):
        self.token = id
    
    def decode(self):
        """ replaces decode method in jwt tokens """
        return self.token # returns user id

def encode_token(user_id):
    """ Generates token for authorization"""

    # Generates testing token
    if app.config.get('TESTING') == True:
        return TestToken(user_id)
    
    payload = {
        'exp': dt.datetime.utcnow() + dt.timedelta(seconds=300),
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
    """Returns token payload"""

    # Decodes testing token
    if app.config.get('TESTING') == True:
        if token in ['Expired Signature','Invalid Token']:
            return TokenPayload(
                valid=False,
                value=token
            )
        else:
            return TokenPayload(
                valid=True,
                value=token
            )
    
    try:
        payload = jwt.decode(
            token,
            secret_key
        )
        # Returns decoded user id in TokenPayload
        return TokenPayload(
            valid=True,
            value=payload['sub']
        )
    except jwt.ExpiredSignatureError:
        return TokenPayload(
            valid=False,
            value='Expired Signature'
        )
    except jwt.InvalidTokenError:
        return TokenPayload(
            valid=False,
            value='Invalid Token'
        )

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
                    password=password)
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
    json_data = request.get_json()
    
    # get token and decode to get payload
    auth_token = json_data['token']
    token_payload = decode_token(auth_token)

    if not token_payload.valid:
        response = {
            'status': 'failure',
            'message': token_payload.value
        }
        return make_response(jsonify(response)), 400
    
    
    # get user from database
    user = User.query.filter_by(id=token_payload.value).first()
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

@api_bp.route('/room', methods=['POST'])
def room_list():
    """ List Rooms using API """
    # Get posted JSON data
    json_data = request.get_json()
    
    # get token and decode to get payload
    auth_token = json_data['token']
    token_payload = decode_token(auth_token)

    if not token_payload.valid:
        response = {
            'status': 'failure',
            'message': token_payload.value
        }
        return make_response(jsonify(response)), 400
    
    # Return chatrooms in JSON
    chatrooms = Chatroom.query.all()
    response = {
        'status':'success',
        #'rooms': {chat.id:chat.name for chat in chatrooms}
        'rooms':[
            {'name':chat.name,'id':chat.id} for chat in chatrooms
        ]
    }
    return make_response(jsonify(response)), 200

@api_bp.route('/room/add', methods=['POST'])
def add_room():
    """ Add Chatroom using API """

    # Get posted JSON data
    json_data = request.get_json()
    
    # get token and decode to get payload
    auth_token = json_data['token']
    token_payload = decode_token(auth_token)

    if not token_payload.valid:
        response = {
            'status': 'failure',
            'message': token_payload.value
        }
        return make_response(jsonify(response)), 400
    
    # get chat room name
    room_name = json_data['room_name']
    
    # check if room with same name exists
    existing_room = Chatroom.query.filter_by(name=room_name).first()
    if existing_room is None:
        # add chat room
        room = Chatroom(name=room_name)
        db.session.add(room)
        db.session.commit()
        response = {
            'status': 'success',
            'message': 'chatroom added.'
        }
        return make_response(jsonify(response)), 200
    # duplicate chat room
    else:
        response = {
            'status': 'failure',
            'message': 'chatroom with that name already exists.'
        }
        return make_response(jsonify(response)), 400

@api_bp.route('/room/<id>', methods=['POST'])
def post_message(id):
    """ post message to chatroom using API """

    # Get posted JSON data
    json_data = request.get_json()
    
    # get token and decode to get payload
    auth_token = json_data['token']
    token_payload = decode_token(auth_token)

    if not token_payload.valid:
        response = {
            'status': 'failure',
            'message': token_payload.value
        }
        return make_response(jsonify(response)), 400
    
    # check if user is a member of chat room
    is_member = MemberList.query.filter_by(
        chatroom_id=id,
        user_id=token_payload.value
        ).first()
    if is_member:
        # get text of message and add to chatroom messages
        text = json_data['text']
        message = Messages(
            chatroom_id=id,
            user_id=token_payload.value,
            text=text
        )
        db.session.add(message)
        db.session.commit()
        response = {
            'status':'success',
            'message': 'added message to chatroom.'
        }
        return make_response(jsonify(response)), 200
    # user is not a member of chatroom
    else:
        response = {
            'status': 'failure',
            'message': 'user is not a member of chatroom.'
        }
        return make_response(jsonify(response)), 403

@api_bp.route('/room/<id>/messages', methods=['POST'])
def get_messages(id):
    """ get messages from chatroom using API """

    # Get posted JSON data
    json_data = request.get_json()
    
    # get token and decode to get payload
    auth_token = json_data['token']
    token_payload = decode_token(auth_token)

    if not token_payload.valid:
        response = {
            'status': 'failure',
            'message': token_payload.value
        }
        return make_response(jsonify(response)), 400
    
    # check if user is a member of chat room
    is_member = MemberList.query.filter_by(
        chatroom_id=id,
        user_id=token_payload.value
        ).first()
    if is_member:
        # get all chat room messages and return them in JSON
        # { time: [username,chat_text], time2: [username,chat_text], ... }
        messages = Messages.query.filter_by(chatroom_id=id).all()
        response = {
            'status':'success',
            'messages': [
                {
                    'id':msg.id,
                    'time':str(msg.ts),
                    'name':msg.user.username,
                    'text':msg.text,
                    'type':(
                        'out' if token_payload.value == msg.user.id else 'in'
                    )
                } for msg in messages
            ]
        }
        return make_response(jsonify(response)), 200
    # user is not a member of chat room
    else:
        response = {
            'status': 'failure',
            'message': 'user is not a member of chatroom.'
        }
        return make_response(jsonify(response)), 403

@api_bp.route('/room/<id>/adduser', methods=['POST'])
def add_user(id):
    """ add user to member list of chatroom using API """

    # Get posted JSON data
    json_data = request.get_json()
    
    # get token and decode to get payload
    auth_token = json_data['token']
    token_payload = decode_token(auth_token)

    if not token_payload.valid:
        response = {
            'status': 'failure',
            'message': token_payload.value
        }
        return make_response(jsonify(response)), 400
    
    # check if user is a member of chat room
    is_member = MemberList.query.filter_by(
        chatroom_id=id,
        user_id=token_payload.value
        ).first()
    # not a member
    if is_member is None:
        # add user to member list for chat room
        member = MemberList(
            user_id = token_payload.value,
            chatroom_id = id)
        db.session.add(member)
        db.session.commit()
        response = {
            'status':'success',
            'message': 'user added to chatroom.'
        }
        return make_response(jsonify(response)), 200
    # is a member
    else:
        response = {
            'status': 'failure',
            'message': 'user is already a member of chatroom.'
        }
        return make_response(jsonify(response)), 400