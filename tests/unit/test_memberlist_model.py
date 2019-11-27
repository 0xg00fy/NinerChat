from application.models import MemberList

def test_new_memberlist():
    """
    Given a Memberlist model
    When a new Memberlist entry is created
    Check that chatroom id and user id are correct
    """

    memberlist = MemberList(
        user_id = 1,
        chatroom_id = 1
    )

    assert memberlist.user_id == 1
    assert memberlist.chatroom_id == 1

