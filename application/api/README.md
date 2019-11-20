
# NinerChat API

## Authentication

Authentication is done by logging in by 

**POST** `/api/login`

**JSON** 
```javascript
{
    'email':email,
    'password':password
}
```

The server will return an authentication token that can be used with further API calls

Currently the authentication tokens are invalid after <u>1 minute</u> for testing/development to make sure tokens do invalidate.

This timeout can be changed in **`/application/api/__init__.py`**:
<details>
<summary>Code</summary>

```python
def encode_token(user_id):
""" Generates token for authorization"""
        
...
        
payload = {
    'exp': dt.datetime.utcnow() + dt.timedelta(minutes=1),
    'iat': dt.datetime.utcnow(),
    'sub': user_id
}
```
</details>

Most API calls are a POST with the authorization token in a **JSON** 
```javascript
{'token': ... , }
```

## Authorization API
<details>
<summary>Sign-up for Account</summary>

__POST__ `/api/signup` 

__JSON__ 
```javascript
{
    'name': name,
    'email': email, 
    'password': password, 
    'college': college, 
    'major': major 
} 
```

__RETURN__
```javascript
{
    status: status,
    message: message,
    token: token
}
```
</details>

<details>
<summary>Login to Account</summary>

__POST__ `/api/login`

__JSON__
```javascript
{
    'email':email,
    'password':password
}
```
__RETURN__
```javascript
{
    token: token ,
}
```
</details>

## Profile API

<details>
<summary>User Profile</summary>

__POST__ `/api/profile`

__JSON__
```javascript
{
    'token':token
}
```
__RETURN__
```javascript
{
    status: status,
    message: message,
    name: name, 
    email: email, 
    college: college, 
    major: major, 
    admin: true or false
}
```
</details>

<details>
<summary>Update Profile</summary>

__POST__ `/api/profile/update`

__JSON__
```javascript
{
    'token': token,
    'name': name,
    'old_password': old_password,
    'password': password,
    'college': college,
    'major': major
}
```
__RETURN__
```javascript
{
    status: status,
    message: message
}
```
</details>

## Room API

<details>
<summary>User's Room List</summary>

__POST__ `/api/room`

__JSON__
```javascript
{
    'token': token
}
```
__RETURN__
```javascript
{
    status: status,
    public_rooms: [
        {
            id: id,
            name: name,
            public: true or false
        },
        ...
    ],
    private_rooms: [
        {
            id: id,
            name: name,
            public: true or false
        },
        ...
    ]
}
```
</details>

<details>
<summary>All Room List</summary>

__POST__ `/api/room/all`

__JSON__
```javascript
{
    'token': token
}
```
__RETURN__
```javascript
{
    status: status,
    public_rooms: [
        {
            id: id,
            name: name,
            public: true or false
        },
        ...
    ],
    private_rooms: [
        {
            id: id,
            name: name,
            public: true or false
        },
        ...
    ]
}
```
</details>

<details>
<summary>Create Room</summary>

__POST__ `/api/room/create`

__JSON__
```javascript
{
    'token': token
    'name': name,
    'public': true or false
}
```
__RETURN__
```javascript
{
    status: status,
    message: message
}
```
</details>

<details>
<summary>Delete Room</summary>

__POST__ `/api/room/<id>/delete`

__JSON__
```javascript
{
    'token': token
}
```
__RETURN__
```javascript
{
    status: status,
    message: message
}
```
</details>

<details>
<summary>Post Message</summary>

__POST__ `/api/room/<id>`

__JSON__
```javascript
{
    'token': token,
    'text': text
}
```
__RETURN__
```javascript
{
    status: status,
    message: message
}
```
</details>

<details>
<summary>Get Messages</summary>

__POST__ `/api/room/<id>/messages`

__JSON__
```javascript
{
    'token': token,
}
```
__RETURN__
```javascript
{
    status: status,
    message: message,
    messages: [
        {
            id:id,
            time:timestamp,
            name:username,
            text:text,
            type: 'out' or 'in'
        },
        ...
    ]
}
```
</details>

<details>
<summary>Subscribe User</summary>

__POST__ `/api/room/<room_id>/subscribe/<user_id>`

__JSON__
```javascript
{
    'token': token    
}
```
__RETURN__
```javascript
{
    status: status,
    message: message
}
```
</details>

<details>
<summary>Unsubscribe User</summary>

__POST__ `/api/room/<room_id>/unsubscribe/<user_id>`

__JSON__
```javascript
{
    'token': token    
}
```
__RETURN__
```javascript
{
    status: status,
    message: message
}
```
</details>

