from application.models import User, Messages, Chatroom, MemberList

def add_user(db):
    user = User.query.filter_by(username='dummy').first()
    chatroom = Chatroom.query.filter_by(name='test').first()
    memberlist = MemberList(
        user_id=user.id,
        chatroom_id=chatroom.id
        )
    db.session.add(memberlist)
    db.session.commit()

def add_message(db):
    user = User.query.filter_by(username='dummy').first()
    chatroom = Chatroom.query.filter_by(name='test').first()
    message = Messages(
        chatroom_id=chatroom.id,
        user_id=user.id,
        text='test'
    )
    db.session.add(message)
    db.session.commit()

def test_get_messages_failure(test_client,init_database,login_json):
    with test_client as c:
        login_response = c.post(
            'http://localhost:5000/api/login',
            json=login_json
        )
        json_data = login_response.get_json()
        token = json_data['token']
        response = c.post(
            'http://localhost:5000/api/room/1/messages',
            json={
                'token':token,
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == 'user is not a member of chatroom.'

def test_get_messages_success(test_client,init_database,login_json):
    with test_client as c:
        add_user(init_database)
        add_message(init_database)
        login_response = c.post(
            'http://localhost:5000/api/login',
            json=login_json
        )
        json_data = login_response.get_json()
        token = json_data['token']
        response = c.post(
            'http://localhost:5000/api/room/1/messages',
            json={
                'token':token,
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['messages'] != None

def test_get_messages_failure(test_client,init_database,expired_token):
    with test_client as c:
        response = c.post(
            'http://localhost:5000/api/room/1/messages',
            json={
                'token':expired_token,
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == expired_token