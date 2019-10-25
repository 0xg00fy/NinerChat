import json
from flask import current_app as app
from flask import Blueprint, request, jsonify, make_response
from . import api_bp, encode_token, decode_token
from application.models import User, Chatroom, MemberList, Messages
from application import db

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
    public_chatrooms = Chatroom.query.filter_by(public=True).all()
    memberlist = MemberList.query.filter_by(user_id=token_payload.value).all()
    private_chatrooms = [item.chatroom for item in memberlist]
    chatrooms = public_chatrooms + private_chatrooms
    response = {
        'status':'success',
        'rooms': {chat.id:[chat.name,chat.public] for chat in chatrooms}
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
    
    # get chat room name and if public
    room_name = json_data['room_name']
    public = json_data['public']
    
    # check if room with same name exists
    existing_room = Chatroom.query.filter_by(name=room_name).first()
    if existing_room is None:
        # add chat room
        room = Chatroom(
            name=room_name,
            public=public)
        db.session.add(room)
        db.session.commit()
        room = Chatroom.query.filter_by(name=room_name).first()
        # make user member of created chatroom
        member = MemberList(
            user_id=token_payload.value,
            chatroom_id=room.id
        )
        db.session.add(member)
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
            'message':is_member.chatroom.name + ' chat messages',
            'room': is_member.chatroom.name,
            'messages': {
                msg.id:[msg.user.username,msg.text,str(msg.ts)] for msg in messages
            }
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