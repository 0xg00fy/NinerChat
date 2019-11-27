from application.models import User, Messages, Chatroom, MemberList

def test_post_message_failure(test_client,init_database,login_json):
    """
    Given an auth token with text
    When check for posting of message to chatroom
    Then check for failure, user not a member, no message text added
    """

    with test_client as c:
        login_response = c.post(
            'http://localhost:5000/api/login',
            json=login_json
        )
        json_data = login_response.get_json()
        token = json_data['token']
        response = c.post(
            'http://localhost:5000/api/room/2',
            json={
                'token':token,
                'text':'test'
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == 'user is not a member of chatroom.'
        assert Messages.query.filter_by(text='test').first() == None

def test_post_message_success(test_client,init_database,admin_login_json):
    """
    Given an auth token with text in JSON
    When check for posting of message to chatroom
    Then check for success, message text added
    """

    with test_client as c:
        login_response = c.post(
            'http://localhost:5000/api/login',
            json=admin_login_json
        )
        json_data = login_response.get_json()
        token = json_data['token']
        response = c.post(
            'http://localhost:5000/api/room/2',
            json={
                'token':token,
                'text':'test'
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['message'] == 'added message to chatroom.'
        assert Messages.query.filter_by(text='test').first() != None

def test_post_message_expired_failure(test_client,init_database,expired_token):
    """
    Given an invalid auth token with text in JSON
    When check for token validity
    Then check for failure, invalid token, no text added
    """
    
    with test_client as c:
        response = c.post(
            'http://localhost:5000/api/room/1',
            json={
                'token':expired_token,
                'text':'test2'
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == expired_token
        assert Messages.query.filter_by(text='test2').first() == None

