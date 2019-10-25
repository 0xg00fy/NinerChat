import json
from flask import current_app as app
from flask import Blueprint, request, jsonify, make_response
from . import api_bp, encode_token, decode_token
from application.models import User
from application import db

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