import json
from flask import current_app as app
from flask import Blueprint, request, jsonify, make_response
from . import api_bp, encode_token, decode_token
from application.models import User, Chatroom, MemberList, Messages
from application import db
from application.room import add_member, delete_member, add_room, delete_room

@api_bp.route('/room', methods=['POST'])
def room_list():
    """ Get the list of rooms the user has membership """
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
    
    # get member list
    memberlist = MemberList.query.filter_by(user_id=token_payload.value).all()
    # get the chatroom from memberlist's chatroom database relationship
    # see models.py for the exact relationship used to perform this
    
    public_chatrooms = [
        item.chatroom for item in memberlist if item.chatroom.public
    ]
    private_chatrooms = [
        item.chatroom for item in memberlist if not item.chatroom.public
    ]
    
    # Return chatrooms in JSON
    response = {
        'status':'success',
        'public_rooms':[
            {
                'name':chat.name,
                'id':chat.id,
                'public':chat.public
            } for chat in public_chatrooms
        ],
        'private_rooms':[
            {
                'name':chat.name,
                'id':chat.id,
                'public':chat.public
            } for chat in private_chatrooms
        ]
    }
    return make_response(jsonify(response)), 200

@api_bp.route('/room/all', methods=['POST'])
def all_room_list():
    """ Get a list of all rooms in database """
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
        'public_rooms':[
            {
                'name':chat.name,
                'id':chat.id,
                'public':chat.public
            } for chat in chatrooms if chat.public
        ],
        'private_rooms':[
            {
                'name':chat.name,
                'id':chat.id,
                'public':chat.public
            } for chat in chatrooms if not chat.public
        ]
    }
    return make_response(jsonify(response)), 200

@api_bp.route('/room/create', methods=['POST'])
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
    name = json_data['name']
    public = json_data['public']
    public = (
        public == 1 or
        public == 'true' or
        public == '1'
    )
    
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

@api_bp.route('/room/<id>/delete', methods=['POST'])
def delete_room(id):
    """
    Delete chatroom from Ninerchat using API
    """
    room = Chatroom.query.filter_by(id=int(id)).first()
    if remove_room(room=room):
        response = {
            'status':'success',
            'message':'chatroom deleted.'
        }
        return make_response(jsonify(response)), 200
    else:
        response = {
            'status': 'failure',
            'message': 'chatroom was not deleted.'
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
    
    user = User.query.filter_by(id=token_payload.value).first()
    room = Chatroom.query.filter_by(id=id).first()

    if not room.public:
        # check if user is a member of chat room
        is_member = MemberList.query.filter_by(
            chatroom_id=id,
            user_id=token_payload.value
            ).first()
    else:
        is_member = True
    
    if is_member or user.admin:
        # get id of last message in database
        last_message = Messages.query.filter_by(chatroom_id=id).order_by(-Messages.id).first()

        if 'msgID' in json_data:
            msg_id = int(json_data['msgID'])
        else:
            msg_id = 0
        
        # if no new messages were posted return empty messages array
        if last_message.id == msg_id:
            response = {
                'status': 'success',
                'message': 'no new messages',
                'messages': []
            }
            return make_response(jsonify(response))
        
        # get all messages after the message id 
        messages = Messages.query.filter_by(chatroom_id=id).filter(
            Messages.id > int(msg_id)
        ).all()

        # return all messages found
        response = {
            'status':'success',
            'message':'messages retrieved',
            'messages': [
                {
                    'id':msg.id,
                    'time':str(msg.ts),
                    'name':msg.user.username,
                    'text':msg.text,
                    'type':(
                        'out' if user_id == msg.user.id else 'in'
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

@api_bp.route('/room/<room_id>/subscribe/<user_id>', methods=['POST'])
def update_members(room_id,user_id):
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

@api_bp.route('/room/<room_id>/unsubscribe/<user_id>', methods=['POST'])
def delete_members(room_id,user_id):
    """
    Remove user from chatroom Memberlist using API
    """
    
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
    
    # get user and chatroom 
    user = User.query.filter_by(id=user_id).first()
    room = Chatroom.query.filter_by(id=room_id).first()

    # remove user from room
    if delete_member(user=user,room=room):
        response = {
            'status':'success',
            'message': 'user removed from chatroom.'
        }
        return make_response(jsonify(response)), 200
    else:
        response = {
            'status': 'failure',
            'message': 'error removing user.'
        }
        return make_response(jsonify(response)), 400