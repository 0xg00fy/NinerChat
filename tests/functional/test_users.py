from application.models import User

def test_new_user():
    """
    Given a User model
    When a new user is created
    Then check the username, email, and password are correct
    """

    user = User(
        username = 'dummy',
        email='dummy@none.com',
        password='password')
    assert user.username == 'dummy'
    assert user.email == 'dummy@none.com'
    assert user.password != 'password'
