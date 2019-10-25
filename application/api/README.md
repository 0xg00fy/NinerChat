
# NinerChat API

## Authentication

Authentication is done by logging in by **POST** `/api/login` with **JSON** `{'email':email, 'password':password}`

The server will return an authentication token that can be used with further API calls

Currently the authentication tokens are invalid after 5 seconds for testing/development to make sure tokens do invalidate.

This timeout can be changed in **api/auth.py**:

    def encode_token(user_id):
    """ Generates token for authorization"""
        
    ...
        
    payload = {
        'exp': dt.datetime.utcnow() + dt.timedelta(seconds=5),
        'iat': dt.datetime.utcnow(),
        'sub': user_id
    }

Most API calls are a **POST** with the token in a **JSON** `{'token': ... , }`

## Sign-up for Account
**POST** `/api/signup` 

**JSON** `{name: , email: , password: , college: , major: }`

**RETURN** `{ status: , message: , token: }`

## Get College Majors List
**GET** `/api/majors`

**RETURN** `{ id:[college,major], id2:[college2,major2], ...}`

*NOTE*: id is a key that can be returned to server and is associated with that college and major if needed

### User Profile
**POST** `/api/profile` 

**JSON** `{ 'token':token }`

**RETURN** `{ status: , message: , name: , email: , college: , major: , admin: }`

### Chat Room List
**POST** `/api/room` 

**JSON** `{ 'token':token }`

**RETURN** `{ id:[name,public] id2:[name2,public2] ... }`

*NOTE*: `id` is chatroom id, `name` is chatroom name, `public` is a boolean for if it is a public chatroom

### Add Chat Room
**POST** `/api/room/add` 

**JSON** `{ token: , room_name: , public: }`

**RETURN** `{ 'status':status, 'message':message }`

### Add User to Chat Room
**POST** `/room/<id>/adduser`

**JSON** `{ 'token':token }`

**RETURN** `{ 'status':status, 'message':message }`

### Post Message to Chat Room
**POST** `/api/room/<id>`

**JSON** `{ 'token':token, 'text':text }`

**RETURN** `{ 'status':status, 'message':message }`

### Get Messages from Chat Room
**POST** `/room/<id>/messages`

**JSON** `{ 'token':token }`

**RETURN** `{ 'status':'status', 'message':message, 'room': name, 'messages': { id:[username,chat_text,timestamp]... } }`