import json
from flask import current_app as app
from flask import Blueprint, request, jsonify, make_response
from . import api_bp, encode_token, decode_token
from application.models import User, Chatroom
from application import db
from application.room import remove_member,add_member, add_room

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
            'email': user.email,
            'college': user.college,
            'major': user.major,
            'admin': user.admin
        }

        return make_response(jsonify(response)), 200

    # user does not exist
    else:
        response = {
            'status': 'failure',
            'message': 'profile not found,'
        }

        return make_response(jsonify(response)), 404

@api_bp.route('/profile/update', methods=['POST'])
def update_profile():
    """
    Update profile using API
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
    
    user = User.query.filter_by(id=token_payload.value).first()
    old_password = json_data['old_password']
    if user.check_password(password=old_password):
        # get user info from JSON
        name = json_data['name']
        password = json_data['password']
        major = json_data['major']
        college = json_data['college']

        # remove user from major and college rooms
        college_room = Chatroom.query.filter_by(
            name=user.college
            ).first()
        major_room = Chatroom.query.filter_by(
            name=user.major
            ).first()
        for room in [college_room,major_room]:
            remove_member(user,room)
        
        # update user info
        user.username = name
        user.set_password(password)
        user.college = college
        user.major = major

        # add user to rooms
        for item in [college,major]:
            add_room(item)
            room = Chatroom.query.filter_by(name=item).first()
            add_member(user,room)
        
        # commit changes to DB
        db.session.commit()
        response = {
            'status': 'success',
            'message': 'profile updated.'
        }
        return make_response(jsonify(response)), 200
    # profile update failed
    else:
        response = {
            'status': 'failure',
            'message': 'old password incorrect, profile not updated.'
        }
        return make_response(jsonify(response)), 400

