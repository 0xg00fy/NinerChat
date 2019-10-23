import json
from flask import current_app as app
from flask import Blueprint, request, jsonify, make_response
from application.api import api_bp, encode_token, decode_token
from application.models import User
from application import db

@api_bp.route('/signup', methods=['POST'])
def signup():
    """User sign-up using API"""
    
    # Get posted JSON data
    signup_data = request.get_json()
    name = signup_data['name']
    email = signup_data['email']
    password = signup_data['password']
    college = signup_data['college']
    major = signup_data['major']
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is None:
        # Create and add user to database
        user = User(username=name,
                    email=email,
                    password=password
                    college=college,
                    major=major)
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

