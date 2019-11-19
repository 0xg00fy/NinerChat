import json
from flask import current_app as app
from flask import Blueprint, request, jsonify, make_response
from . import api_bp, encode_token, decode_token
from application.models import User, Chatroom, MemberList, Messages
from application import db
from application.room import add_member, add_room

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
def create_room():
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
    
    # get chat room name and if public
    name = json_data['room_name']
    public = json_data['public']
    
    # get user id
    user_id = token_payload.value
    
    # try to add chatroom
    if add_room(name=name,public=int(public)):
        user = User.query.filter_by(id=user_id).first()
        room = Chatroom.query.filter_by(name=name).first()
        add_member(user=user,room=room)
        response = {
            'status':'success',
            'message':'chatroom added.'
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
    
    user = User.query.filter_by(id=token_payload.value).first()
    # check if user is a member of chat room
    if user.admin:
        is_member = True
    else:
        is_member = MemberList.query.filter_by(
            chatroom_id=id,
            user_id=user.id
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

@api_bp.route('/room/<room_id>/add_member', methods=['POST'])
def add_user(room_id):
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
    
    user_id = json_data['user_id']
    user = User.query.filter_by(id=int(user_id)).first()
    room = Chatroom.query.filter_by(id=int(room_id)).first()
    
    if add_member(user=user,room=room):
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