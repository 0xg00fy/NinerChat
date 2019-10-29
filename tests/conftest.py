import pytest

from application import create_app, db
from application.models import User, Chatroom
from config import TestConfig
import flask_login

@pytest.fixture(scope='module')
def new_user():
    """
    Creates user with no admin rights.
    Use to test regular users.
    """
    user = User(
        username='dummy',
        email='dummy@uncc.edu',
        password='dummy',
        college='Computing and Informatics',
        major='Computer Science')
    return user

@pytest.fixture(scope='module')
def new_admin():
    """
    Creates user with admin rights.
    Use to test admin users.
    """
    admin_user = User(
        username='admin',
        email='ninerchat@uncc.edu',
        password='admin',
        admin=True)
    return admin_user

@pytest.fixture(scope='module')
def new_public_chatroom():
    """
    Creates public chatroom with name 'test'
    Use to test public chatrooms
    """
    chatroom = Chatroom(
        name = 'test',
        public = True
    )
    return chatroom

@pytest.fixture(scope='module')
def new_private_chatroom():
    """
    Creates public chatroom with name 'test'
    Use to test public chatrooms
    """
    chatroom = Chatroom(
        name = 'test',
        public = False
    )
    return chatroom

@pytest.fixture(scope='module')
def login_json():
    return {
        'email':'dummy@uncc.edu',
        'password':'dummy'
    }

@pytest.fixture(scope='module')
def expired_token():
    return 'Expired Signature'

@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestConfig)

    test_app = app.test_client()

    context = app.app_context()
    context.push()

    yield test_app

    context.pop()

@pytest.fixture(scope='module')
def init_database(new_user,new_public_chatroom):
    db.create_all()

    # add user
    db.session.add(new_user)
    # add public chatroom
    db.session.add(new_public_chatroom)
    db.session.commit()

    yield db

    db.drop_all()

@pytest.fixture(scope='module')
def admin_login_client(test_client):
    with test_client as c:
        response = c.post(
            'http://localhost:5000/login',
            data={
                'email':'ninerchat@uncc.edu',
                'password':'admin'
            },
            follow_redirects=True
        )
        yield c
