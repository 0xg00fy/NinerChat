
def test_login_success(test_client,init_database,login_json):
    """
    Given an email and password in JSON
    When check for valid credentials
    Then check for success, auth token returned
    """
    with test_client as c:
        response = c.post(
            '/api/login',
            json=login_json
        )
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['message'] == 'sucessfully logged in.'
        assert json_data['token'] != None

def test_login_failure(test_client, init_database):
    """
    Given a wrong email or wrong password in JSON
    When check for valid credentials
    Then check for failure, message
    """

    with test_client as c:
        # wrong password
        response = c.post(
            '/api/login',
            json={
                'email':'dummy@none.com',
                'password':'wrongpassword'
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == 'email or password incorrect.'

        # wrong email
        response = c.post(
            '/api/login',
            json={
                'email':'wrong@none.com',
                'password':'dummy'
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == 'email or password incorrect.'