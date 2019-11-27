from flask_login import current_user
from application.models import User
from flask import url_for, request, flash

def test_signup_success(test_client):
    """
    Given unique email, name, password
    When check for user sign up
    Then check for success, user added, chat room membership
    """

    with test_client as c:
        response = c.post(
            'http://localhost:5000/signup',
            data={
                'name':'dummy2',
                'email':'dummy2@uncc.edu',
                'password':'password',
                'confirm':'password',
                'major':'0'
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        user = User.query.filter_by(username='dummy2').first()
        assert user != None
        assert user.email == 'dummy2@uncc.edu'
        assert request.path == url_for('main_bp.chat')


def test_signup_failure(test_client,init_database):
    """
    Given duplicate email, name, password
    When check for user sign up
    Then check for failure, user not added
    """
    
    with test_client as c:
        response = c.post(
            '/signup',
            data={
                'name':'dummy',
                'email':'dummy@uncc.edu',
                'password':'password',
                'confirm':'password',
            }
        )
        assert response.status_code != 200
        assert request.path == url_for('auth_bp.signup_page')