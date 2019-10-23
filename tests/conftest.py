import pytest

from application import create_app, db
from application.models import User, Chatroom
from config import TestConfig

@pytest.fixture(scope='module')
def new_user():
    """
    Creates user with no admin rights.
    Use to test regular users.
    """
    user = User(
        username='dummy',
        email='dummy@none.com',
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
        email='admin@none.com',
        password='admin',
        admin=True)
    return admin_user

@pytest.fixture(scope='module')
def login_json():
    return {
        'email':'dummy@none.com',
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
def init_database():
    db.create_all()

    # add dummy user
    user = User(
        username='dummy',
        email='dummy@none.com',
        password='dummy')
    db.session.add(user)
    db.session.commit()

    # add chatroom
    chatroom = Chatroom(
        name = 'test'
    )
    db.session.add(chatroom)
    db.session.commit()

    yield db

    db.drop_all()
