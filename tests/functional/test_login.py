from flask_login import current_user

def test_login_failure(test_client):
    """
    given a default admin
    When incorrect admin credentials are posted
    Check that login fails
    """
    with test_client as c:
        response = c.post(
            'http://localhost:5000/login',
            data={
                'email':'ninerchat@uncc.edu',
                'password':'wrong'
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert current_user.get_id() == None
        assert current_user.is_authenticated == False

def test_login_success(test_client):
    """
    Given a default admin
    When admin login credentials are posted
    Then check that admin login successfully
    """
    with test_client as c:
        response = c.post(
            'http://localhost:5000/login',
            data={
                'email':'ninerchat@uncc.edu',
                'password':'admin'
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert current_user.get_id() != None
        assert current_user.is_authenticated == True