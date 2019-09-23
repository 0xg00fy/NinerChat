"""Routes for user authentication."""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash
from .forms import AddRoomForm
from .models import db, User, Chatroom, MemberList, Messages
from . import login_manager

# Blueprint Configuration
room_bp = Blueprint('room_bp', __name__,
    url_prefix='/room',
    template_folder='templates',
    static_folder='static')

@room_bp.route('/', methods=['GET'])
@login_required
def list_rooms():
    """List rooms"""
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
    """Add room to NinerChat"""
    room_form = AddRoomForm(request.form)
    if request.method == 'POST' and room_form.validate():
        name = request.form.get('name')
        existing_room = Chatroom.query.filter_by(name=name).first()
        if existing_room is None:
            room = Chatroom(
                name=name
            )
            db.session.add(room)
            db.session.commit()
            return redirect(url_for('room_bp.list_rooms'))
        else:
            flash('A room already exists with that name')
            return redirect(url_for('room_bp.add_room'))
    elif request.method == 'GET':
        return render_template('add_room.html',
            title='NinerChat | Create ChatRoom',
            form=AddRoomForm(),
            template='addroom-page',
            body='Add a Room to NinerChat')
    else:
        for field, errors in room_form.errors.items():
            flash(u'%s - %s' % (room_form[field].label.text, ','.join(errors)))
        return redirect(url_for('room_bp.add_room'))

@room_bp.route('/<id>')
@login_required
def show(id):
    room = Chatroom.query.filter_by(id=id).first()
    return 'Displaying %r' % (room.name)

@room_bp.route('/<id>/members')
@login_required
def show_members(id):
    members = MemberList.query.filter_by(chatroom_id=id).all()
    names = ' '.join([member.user.username for member in members])
    return names

@room_bp.route('<id>/adduser')
@login_required
def adduser(id):
    existing_user = MemberList.query.filter_by(user_id=current_user.id).first()
    if existing_user is None:
        member = MemberList(
            user_id = current_user.id,
            chatroom_id = id)
        db.session.add(member)
        db.session.commit()
    return redirect(url_for('room_bp.show_members', id=id))
