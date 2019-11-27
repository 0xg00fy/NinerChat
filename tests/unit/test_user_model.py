from application.models import User

def test_new_user(new_user):
    """
    Given a User model
    When a new User is created
    Then check the username, email, password, admin rights are correct
    """
    assert new_user.username=='dummy'
    assert new_user.email=='dummy@uncc.edu'
    assert new_user.password != 'dummy' # check if hashed
    assert new_user.admin == False
    assert new_user.college == 'Computing and Informatics'
    assert new_user.major == 'Computer Science'

def test_new_admin(new_admin):
    """
    Given a User model
    When a new User is created
    Then check the username, email, password, admin rights are correct
    """
    assert new_admin.username=='admin'
    assert new_admin.email=='ninerchat@uncc.edu'
    assert new_admin.password != 'admin' # check if hashed
    assert new_admin.admin == True
    assert new_admin.college == 'None'
    assert new_admin.major == 'Undecided'

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

def test_incorrect_college():
    """
    Given a new User
    When the college or major is incorrect
    Then the college and major is set to None and Undecided
    """
    user = User(
        username='newuser',
        email='newuser@uncc.edu',
        password='password',
        college='Wrong',
        major='Bad'
    )
    assert user.college != 'Wrong'
    assert user.major != 'Bad'
    assert user.college == 'None'
    assert user.major == 'Undecided'