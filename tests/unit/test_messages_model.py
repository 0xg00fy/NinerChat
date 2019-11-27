from application.models import Messages
#from datetime import datetime

def test_new_message():
    """
    Given a Messages model
    When a new message is created
    Check that the timestamp, chatroom,user id, and text are correct
    """

    message = Messages(
        chatroom_id=1,
        user_id=1,
        text='test',
    )
    assert message.chatroom_id==1
    assert message.user_id==1
    assert message.text=='test'
    # figure out how to test datetime