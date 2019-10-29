from application.models import Blacklist

def test_new_blacklist():
    """
    Given a Blacklist model
    When a new Blacklist is created
    Check the the user id and reason are correct
    """
    blacklist = Blacklist(
        user_id=1,
        reason='reasons'
    )

    assert blacklist.user_id == 1
    assert blacklist.reason == 'reasons'