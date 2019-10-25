from application.models import Chatroom

def test_room_add_success(test_client,init_database,login_json):
    """
    Given a valid auth token and room name
    When check for room added
    Then check for success, new room added with name
    """

    with test_client as c:
        login_response = c.post(
            'http://localhost:5000/api/login',
            json=login_json
        )
        json_data = login_response.get_json()
        token = json_data['token']
        response = c.post(
            'http://localhost:5000/api/room/add',
            json={
                'token': token,
                'room_name': 'test2',
                'public': True
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['message'] == 'chatroom added.'
        assert Chatroom.query.filter_by(name='test2').first() != None

def test_room_add_failure(test_client,init_database,login_json):
    """
    Given a valid auth token and duplicate room name
    When check for room added
    Then check for failure, duplicate room not added
    """

    with test_client as c:
        login_response = c.post(
            'http://localhost:5000/api/login',
            json=login_json
        )
        json_data = login_response.get_json()
        token = json_data['token']
        response = c.post(
            'http://localhost:5000/api/room/add',
            json={
                'token': token,
                'room_name': 'test',
                'public': True
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == 'chatroom with that name already exists.'