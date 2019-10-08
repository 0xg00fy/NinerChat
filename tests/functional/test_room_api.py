
def test_room_list_success(test_client, init_database):
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
            'http://localhost:5000/api/room',
            json={
                'token': token
            }
        )
        json_data = profile_response.get_json()
        assert json_data['status'] == 'success'
        assert 'test' in json_data['rooms'].values()

def test_room_list_failure(test_client, init_database):
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
            'http://localhost:5000/api/room',
            json={
                'token': 'Expired Signature' #Invalid token
            }
        )
        json_data = profile_response.get_json()
        assert json_data['status'] == 'failure'
