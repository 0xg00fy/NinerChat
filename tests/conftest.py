import pytest

from application import create_app, db
from application.models import User, Chatroom
from config import TestConfig

@pytest.fixture(scope='module')
def new_user():
    user = User(
        username='dummy',
        email='dummy@none.com',
        password='dummy')
    return user


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
