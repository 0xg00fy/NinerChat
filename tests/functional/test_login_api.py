
def test_login_success(test_client, init_database):
    with test_client as c:
        response = c.post(
            '/api/login',
            json={
                'email':'dummy@none.com',
                'password':'dummy'
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['message'] == 'sucessfully logged in.'
        assert json_data['token'] != None

def test_login_failure(test_client, init_database):
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