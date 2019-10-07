import requests

def test_signup_success(test_client):
    with test_client as c:
        response = c.post(
            '/api/signup',
            json={
                'name':'dummy2',
                'email':'dummy2@none.com',
                'password':'dummy2'
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['message'] == 'successfully registered.'
        assert json_data['token'] != None

def test_signup_failure(test_client,init_database):
    with test_client as c:
        response = c.post(
            '/api/signup',
            json={
                'name':'dummy',
                'email':'dummy@none.com',
                'password':'dummy'
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == 'could not be registered.'