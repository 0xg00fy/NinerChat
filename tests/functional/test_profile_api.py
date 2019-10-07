
def test_profile_success(test_client, init_database):
    with test_client as c:
        login_response = c.post(
            'http://localhost:5000/api/login',
            json={
                'email':'dummy@none.com',
                'password':'dummy'
            }
        )
        json_data = login_response.get_json()
        token = json_data['token']
        profile_response = c.post(
            'http://localhost:5000/api/profile',
            json={
                'token': token
            }
        )
        json_data = profile_response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['name'] == 'dummy'
        assert json_data['email'] == 'dummy@none.com'

def test_profile_failure(test_client, init_database):
    with test_client as c:
        token = 'Expired Signature'
        profile_response = c.post(
            'http://localhost:5000/api/profile',
            json={
                'token': token
            }
        )
        json_data = profile_response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == 'Expired Signature'
        