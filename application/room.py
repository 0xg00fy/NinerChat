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
    public_chatrooms = [
        room for room in chatrooms if room.public
    ]
    private_chatrooms = [
        room for room in chatrooms if not room.public
    ]
    return render_template('list_rooms.html',
        title='NinerChat | Room List',
        template='room-list',
        user=current_user,
        public_chatrooms=public_chatrooms,
        private_chatrooms=private_chatrooms
        )

@room_bp.route('/create', methods=['GET','POST'])
@login_required
def create_room():
    """
    Add chatroom to NinerChat
    """
    room_form = AddRoomForm(request.form)
    if request.method == 'POST' and room_form.validate():
        # get form data
        name = request.form.get('name')
        public = request.form.get('public')
        
        # add room if possible
        if add_room(name=name,public=int(public)):
            # add current user to new room
            user = current_user
            room = Chatroom.query.filter_by(name=name).first()
            add_member(user=user,room=room)
            # return to main
            return redirect(url_for('main_bp.chat'))
        else:
            flash('A room already exists with that name')
            return redirect(url_for('room_bp.create_room'))
    elif request.method == 'GET' and current_user.admin:
        # get form
        return render_template('add_room.html',
            title='NinerChat | Create ChatRoom',
            form=AddRoomForm(),
            template='addroom-page',
            body='Add a Room to NinerChat')
    else:
        for field, errors in room_form.errors.items():
            flash(u'%s - %s' % (room_form[field].label.text, ','.join(errors)))
        return redirect(url_for('room_bp.create_room'))

@room_bp.route('/<room_id>/delete', methods=['GET'])
@login_required
def delete_room(room_id):
    """
    Delete chatroom from Ninerchat
    """
    room = Chatroom.query.filter_by(id=int(room_id)).first()
    if remove_room(room=room):
        flash('Chatroom deleted')
    else:
        flash('Error deleting room')
    return redirect(url_for('main_bp.chat'))


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
        is_member = MemberList.query.filter_by(
                chatroom_id=id, user_id=current_user.id
                ).first()
        # check if public room or admin user
        if current_user.admin and is_member is None:
            add_member(current_user,room)
            is_member = True
        elif room.public and is_member is None:
            add_member(current_user,room)
            is_member = True
        
        if is_member is None:
            flash('User not a member of private chat %s' % room.name)
            return redirect(next or url_for('main_bp.chat'))

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
def read_members(id):
    """
    Shows the member list for the chatroom
    """
    members = MemberList.query.filter_by(chatroom_id=id).all()
    names = ' '.join([member.user.username for member in members])
    return names

@room_bp.route('<room_id>/subscribe/<user_id>')
@login_required
def update_members(room_id,user_id):
    """
    Adds user to chatroom MemberList
    """
    user = User.query.filter_by(id=user_id).first()
    room = Chatroom.query.filter_by(id=room_id).first()
    if add_member(user=user,room=room):
        flash('user added')
    else:
        flash('error adding user')
    return redirect(request.referrer)

@room_bp.route('<room_id>/unsubscribe/<user_id>')
@login_required
def delete_member(room_id,user_id):
    """
    Remove user from chatroom MemberList
    """
    user = User.query.filter_by(id=user_id).first()
    room = Chatroom.query.filter_by(id=room_id).first()
    if remove_member(user=user,room=room):
        flash('user removed')
    else:
        flash('error removing user')
    return redirect(request.referrer)


def add_member(user=User,room=Chatroom):
    existing_user = MemberList.query.filter_by(
        user_id = user.id,
        chatroom_id = room.id
        ).first()
    if existing_user is None:
        member = MemberList(
            user_id = user.id,
            chatroom_id = room.id
        )
        db.session.add(member)
        db.session.commit()
        return True
    else:
        return False

def remove_member(user=User,room=Chatroom):
    member = MemberList.query.filter_by(
        user_id=user.id,
        chatroom_id=room.id
        ).first()
    if member is None:
        return False
    else:
        db.session.delete(member)
        db.session.commit()
        return True

def add_room(name=str,public=False):
    existing_room = Chatroom.query.filter_by(name=name).first()
    if existing_room is None:
        room = Chatroom(
            name=name,
            public=int(public)
        )
        db.session.add(room)
        db.session.commit()
        return True
    else:
        return False

def remove_room(room=Chatroom):
    members = MemberList.query.filter_by(chatroom_id=room.id).all()
    messages = Messages.query.filter_by(chatroom_id=room.id).all()
    if members != None:
        for member in members:
            db.session.delete(member)
    if messages != None:
        for message in messages:
            db.session.delete(message)
    db.session.delete(room)
    db.session.commit()
    return True
