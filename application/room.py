"""Routes for Chat Rooms"""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash
from .forms import AddRoomForm, ChatPostForm
from .models import db, User, Chatroom, MemberList, Messages
from . import login_manager

# Blueprint Configuration
room_bp = Blueprint('room_bp', __name__,
    url_prefix='/room',
    template_folder='templates',
    static_folder='static')

@room_bp.route('/', methods=['GET'])
def list_rooms():
    """
    Lists all chatrooms that are in database
    """
    chatrooms = Chatroom.query.all()
    return render_template('list_rooms.html',
        title='NinerChat | Room List',
        template='room-list',
        user=current_user,
        chatrooms=chatrooms,
        )

@room_bp.route('/add', methods=['GET','POST'])
@login_required
def add_room():
    """
    Add chatroom to NinerChat
    """
    room_form = AddRoomForm(request.form)
    if request.method == 'POST' and room_form.validate():
        name = request.form.get('name')
        public = request.form.get('public')
        existing_room = Chatroom.query.filter_by(name=name).first()
        if existing_room is None:
            room = Chatroom(
                name=name,
                public=int(public)
            )
            db.session.add(room)
            db.session.commit()
            # add user to memberlist if private
            if not room.public:
                chatroom = Chatroom.query.filter_by(name=name).first()
                member = MemberList(
                    user_id = current_user.id,
                    chatroom_id = chatroom.id
                )
                db.session.add(member)
                db.session.commit()
            return redirect(url_for('main_bp.chat'))
        else:
            flash('A room already exists with that name')
            return redirect(url_for('room_bp.add_room'))
    elif request.method == 'GET' and current_user.admin:
        return render_template('add_room.html',
            title='NinerChat | Create ChatRoom',
            form=AddRoomForm(),
            template='addroom-page',
            body='Add a Room to NinerChat')
    else:
        for field, errors in room_form.errors.items():
            flash(u'%s - %s' % (room_form[field].label.text, ','.join(errors)))
        return redirect(url_for('room_bp.add_room'))

@room_bp.route('/<id>', methods=['GET','POST'])
@login_required
def show(id):
    """
    Displays chatroom with messages and ability to post
    new messages to the chatroom
    """
    chat_post_form = ChatPostForm(request.form)
    if request.method == 'POST' and chat_post_form.validate():
        text = request.form.get('text')
        message = Messages(
            chatroom_id=id,
            user_id=current_user.id,
            text=text)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('room_bp.show',id=id))
    elif request.method == 'GET':
        room = Chatroom.query.filter_by(id=id).first()
        if room is None:
            flash('Room does not exist!')
            return redirect(url_for('main_bp.chat'))
        # check if public room or admin user
        if room.public or current_user.admin:
            is_member = True
        else:
            is_member = MemberList.query.filter_by(
                chatroom_id=id, user_id=current_user.id
                ).first()
        if is_member is None:
            flash('User not a member of private chat %s' % room.name)
            return redirect(next or url_for('main_bp.chat'))
            
            # return render_template('add_user.html',
            #     title='NinerChat | Add User to ChatRoom',
            #     template='add-user-chatroom',
            #     body='Add User',
            #     user=current_user,
            #     room=room)

        else:
            messages = Messages.query.filter_by(chatroom_id=id).all()
            return render_template('show_chatroom.html',
                title='NinerChat | View ChatRoom',
                template='view-chatroom',
                body=room.name,
                form=ChatPostForm(),
                user=current_user,
                messages=messages,
                room=room)
    else:
        return "Something went wrong!"

@room_bp.route('/<id>/members')
@login_required
def show_members(id):
    """
    Shows the member list for the chatroom
    """
    members = MemberList.query.filter_by(chatroom_id=id).all()
    names = ' '.join([member.user.username for member in members])
    return names

@room_bp.route('<id>/adduser')
@login_required
def adduser(id):
    """
    Adds user to chatroom memberlist
    """
    existing_user = MemberList.query.filter_by(user_id=current_user.id,chatroom_id=id).first()
    if existing_user is None:
        member = MemberList(
            user_id = current_user.id,
            chatroom_id = id)
        db.session.add(member)
        db.session.commit()
    return redirect(url_for('room_bp.show', id=id))
