from application.models import MemberList

def test_add_user_success(test_client,init_database,login_json):
    with test_client as c:
        login_response = c.post(
            'http://localhost:5000/api/login',
            json=login_json
        )
        json_data = login_response.get_json()
        token = json_data['token']
        response = c.post(
            'http://localhost:5000/api/room/1/adduser',
            json={
                'token':token,
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['message'] == 'user added to chatroom.'
        is_member = MemberList.query.filter_by(
            user_id=token,
            chatroom_id=1
            ).first()
        assert is_member != None

def test_add_user_failure(test_client,init_database,login_json):
    with test_client as c:
        login_response = c.post(
            'http://localhost:5000/api/login',
            json=login_json
        )
        json_data = login_response.get_json()
        token = json_data['token']
        response = c.post(
            'http://localhost:5000/api/room/1/adduser',
            json={
                'token':token,
            }
        )
        json_data = response.get_json()
        assert json_data['status'] == 'failure'
        assert json_data['message'] == 'user is already a member of chatroom.'
        is_member = MemberList.query.filter_by(
            user_id=token,
            chatroom_id=1
            ).first()
        assert is_member != None
