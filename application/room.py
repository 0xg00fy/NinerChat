"""Routes for Chat Rooms"""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash
from .forms import AddRoomForm, ChatPostForm, SelectRoomForm, SelectPublicRoomForm, SelectPrivateRoomForm
from .models import db, User, Chatroom, MemberList, Messages
from . import login_manager
from flask import jsonify, make_response
import json


# Blueprint Configuration
room_bp = Blueprint('room_bp', __name__,
    url_prefix='/room',
    template_folder='templates',
    static_folder='static')

@room_bp.route('/', methods=['GET','POST'])
def list_rooms():
    """
    Lists all chatrooms that are in database
    """
    private_room_select = SelectPrivateRoomForm(request.form)
    public_room_select = SelectPublicRoomForm(request.form)

    filter=request.args.get('filter')
    if filter == 'private' and current_user.admin:
        form = SelectPrivateRoomForm()
    else:
        form = SelectPublicRoomForm()
    
    if request.method == 'POST':
        room_id = request.form.get('room_id')
        return redirect(url_for(
            'room_bp.show',
            id=room_id
        ))
    
    elif request.method == 'GET':
        
        return render_template('list_rooms.html',
            title='NinerChat | Room List',
            template='room-list',
            user=current_user,
            form=form,
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

@room_bp.route('/<id>/delete', methods=['GET'])
@login_required
def delete_room(id):
    """
    Delete chatroom from Ninerchat
    """
    room = Chatroom.query.filter_by(id=int(id)).first()
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
                js_func='startChat();',
                body=room.name,
                form=ChatPostForm(),
                user=current_user,
                messages=messages,
                room=room)
    else:
        return "Something went wrong!"

@room_bp.route('/<id>/messages', methods=['POST','GET'])
def get_messages(id):
    """
    Retrieves messages for chatroom

    Post last message id and if there are no new messages, returns nothing, and
    if there are new messages, returns only the new messages.
    Otherwise returns all messages
    """
    # get last
    last_message = Messages.query.filter_by(chatroom_id=id).order_by(-Messages.id).first()
    if request.method == "GET":
        return str(last_message.id)
    else:
        # get JSON data
        json_data = request.get_json()
        if 'msg_id' in json_data:
            msg_id = int(json_data['msg_id'])
        else:
            msg_id = 0
        if 'user_id' in json_data:
            user_id = int(json_data['user_id'])
        else:
            response = {'status':'failure','message':'no user_id'}
            return make_response(jsonify(response)), 400
        
        if last_message.id == msg_id:
            response = {
                'status': 'success',
                'message': 'no new messages',
                'messages': []
            }
            return make_response(jsonify(response))

        messages = Messages.query.filter_by(chatroom_id=id).filter(
            Messages.id > int(msg_id)
        ).all()
        response = {
            'status':'success',
            'message':'messages retrieved',
            'messages': [
                {
                    'id':msg.id,
                    'time':str(msg.ts),
                    'name':msg.user.username,
                    'text':msg.text,
                    'type':(
                        'out' if user_id == msg.user.id else 'in'
                    )
                } for msg in messages
            ]
        }
        return make_response(jsonify(response)), 200
            
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
    if user is None or room is None:
        return False
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
