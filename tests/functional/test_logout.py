from flask_login import logout_user, current_user

def test_logout_success(admin_login_client):
    c = admin_login_client
    assert current_user.get_id() != None
    c.get(
        'http://localhost:5000/logout',
        follow_redirects=True
    )
    assert current_user.get_id() == None