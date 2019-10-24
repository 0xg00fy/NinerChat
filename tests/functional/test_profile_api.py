
def test_profile_success(test_client, init_database,login_json):
    """
    Given an valid auth token
    When check for profile info
    Then check for success, profile data returned in JSON
    """

    with test_client as c:
        login_response = c.post(
            'http://localhost:5000/api/login',
            json=login_json
        )
        json_data = login_response.get_json()
        token = json_data['token']
        response = c.post(
            'http://localhost:5000/api/profile',
            json={'token': token}
        )
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['name'] == 'dummy'
        assert json_data['email'] == 'dummy@uncc.edu'

def test_profile_failure(test_client, init_database, expired_token):
    """
    Given an invalid auth token
    When check for profile info
    Then check for failure, expired token
    """

    with test_client as c:
        response = c.post(
            'http://localhost:5000/api/profile',
            json={'token': expired_token}
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == expired_token
        