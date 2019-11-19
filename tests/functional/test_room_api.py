
def test_room_list_success(test_client, init_database,login_json):
    """
    Given a valid auth token
    When check for room list
    Then check for success, room list
    """

    with test_client as c:
        login_response = c.post(
            'http://localhost:5000/api/login',
            json=login_json
        )
        json_data = login_response.get_json()
        token = json_data['token']
        response = c.post(
            'http://localhost:5000/api/room',
            json={'token': token}
        )
        json_data = response.get_json()
        assert json_data['status'] == 'success'

def test_room_list_failure(test_client,init_database, expired_token):
    """
    Given an invalid auth token
    When check for room list
    Then check for failure, no room list
    """

    with test_client as c:
        response = c.post(
            'http://localhost:5000/api/room',
            json={'token': expired_token}
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == expired_token
