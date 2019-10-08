# NinerChat

## Installation Instructions
`python3 -m venv env`\
`source env/bin/activate`\
`pip install -r requirements.txt`

## Running Flask App

Linux/MacOs:

`source env/bin/activate`\
`bash start.sh`\
`deactivate`

Windows:

`env\Scripts\activate`\
`start.bat`\
`deactivate`

## API

### Authentication

Authentication is done by logging in by POST `/api/login` with JSON `{'email':email, 'password':password}`

The server will return an authentication token that can be used with further API calls

Currently the authentication tokens are invalid after 5 seconds for testing/development to make sure tokens do invalidate.

This timeout can be changed in **application/auth.py**:

    def encode_token(user_id):
    """ Generates token for authorization"""
        
    ...
        
    payload = {
        'exp': dt.datetime.utcnow() + dt.timedelta(seconds=5),
        'iat': dt.datetime.utcnow(),
        'sub': user_id
    }

Most API calls are a POST with the token in a JSON `{'token': ... , }`

### Sign-up for Account
POST `/api/signup` 

JSON `{ 'name':name, 'email':email, 'password':password }`

RETURN `{ 'status':status, 'message':message, 'token':token }`

### User Profile
POST `/api/signup` 

JSON `{ 'token':token }`

RETURN `{ 'status':status, 'message':message, 'name':name, 'email': email }`

### Chat Room List
POST `/api/room` 

JSON `{ 'token':token }`

RETURN `{ id:name, id2:name2, ... }`

### Add Chat Room
POST `/api/room/add` 

JSON `{ 'token':token, 'room_name':name }`

RETURN `{ 'status':status, 'message':message }`

### Add User to Chat Room
POST `/room/<id>/adduser`

JSON `{ 'token':token }`

RETURN `{ 'status':status, 'message':message }`

### Post Message to Chat Room
POST `/api/room/<id>`

JSON `{ 'token':token, 'text':text }`

RETURN `{ 'status':status, 'message':message }`

### Get Messages from Chat Room
POST `/room/<id>/messages`

JSON `{ 'token':token }`

RETURN `{ 'time': [username,chat_text], 'time2': [username,chat_text], ... }`