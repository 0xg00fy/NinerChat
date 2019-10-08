# @pytest.fixture(scope='module')
# def add_user():
#     user = User.query.filter_by(username='dummy').first()
#     chatroom = Chatroom.query.filter_by(name='test').first()
#     memberlist = MemberList(
#         user_id=user.id,
#         chatroom_id=chatroom.id
#         )
#     db.session.add(memberlist)
#     db.session.commit()