from application.models import Chatroom

def test_new_public_chatroom(new_public_chatroom):
    """
    Given a Chatroom model
    When a new chatroom is created
    Check the name and public/private status
    """
    assert new_public_chatroom.name == 'public-test'
    assert new_public_chatroom.public == True

def test_new_private_chatroom(new_private_chatroom):
    """
    Given a Chatroom model
    When a new chatroom is created
    Check the name and public/private status
    """
    assert new_private_chatroom.name == 'private-test'
    assert new_private_chatroom.public == False
