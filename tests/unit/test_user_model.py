
def test_new_user(new_user):
    """
    Given a User model
    When a new User is created
    Then check the username, email, password, are correct
    """
    assert new_user.username=='dummy'
    assert new_user.email=='dummy@none.com'
    assert new_user.password != 'dummy' # check if hashed

def test_setting_password(new_user):
    """
    Given an existing User
    When the password for the user is set
    Then check the password is stored correctly as hash
    """
    new_user.set_password('newpassword')
    assert new_user.password != 'newpassword'
    assert new_user.check_password('newpassword')
    assert not new_user.check_password('dummy')
    assert not new_user.check_password('otherpassword')
