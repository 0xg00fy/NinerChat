"""Dashboard for the ninerchat server"""
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user
from flask import current_app as app
from application.auth import admin_only
from application.forms import SelectRoomForm
from application.models import db, User, Chatroom, MemberList, Messages
from flask_login import login_required

# Blueprints
dashboard_bp = Blueprint('dashboard_bp', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/admin')

@dashboard_bp.route('/')
@admin_only
def main():
    """ Main dashboard """
    return render_template('main_dashboard.html',
        title='NinerChat | Admin Dashboard',
        template='admin-dashboard',
        current_user=current_user,
        body="Admin Dashboard")

@dashboard_bp.route('/users')
@admin_only
def user():
    """ User dashboard """
    users = User.query.all()
    sort_by = request.args.get('sort')
    user_list = [
        {
            'id':u.id,
            'name':u.username,
            'email':u.email,
            'college':u.college,
            'major':u.major
        } for u in users
    ]
    if sort_by:
        user_list.sort(key=lambda x: x[sort_by])
    
    return render_template('user_dashboard.html',
        title='NinerChat | User Dashboard',
        template='user-dashboard',
        current_user=current_user,
        users=user_list,
        body="User Dashboard")

@dashboard_bp.route('/users/<id>', methods=['GET','POST'])
@admin_only
def user_profile(id):
    """ User profile for admins """

    room_select = SelectRoomForm(request.form)

    if request.method == 'POST' and room_select.validate():
        room_id = request.form.get('room_id')
        user_id = id
        return redirect(url_for(
            'room_bp.update_members',
            room_id=room_id,
            user_id=user_id
        ))
    elif request.method == 'GET':
        user = User.query.filter_by(id=int(id)).first()
        memberlist = MemberList.query.filter_by(user_id=int(id)).all()
        rooms = Chatroom.query.all()
        room_list = [
            (room.id,room.name) for room in rooms 
        ]

        return render_template('user_profile_dashboard.html',
            title='NinerChat | User Profile',
            template='user-profile-dashboard',
            current_user=current_user,
            user=user,
            memberlist=memberlist,
            form=SelectRoomForm(),
            body="User Profile Dashboard")

@dashboard_bp.route('/users/<id>/messages', methods=['GET','POST'])
@admin_only
def user_messages(id):
    """ User messages for admins """
    user = User.query.filter_by(id=id).first()
    messages = Messages.query.filter_by(user_id=int(id)).all()
    messages_list = [
        {
            'id':int(m.id),
            'ts':str(m.ts),
            'chatroom_id':m.chatroom_id,
            'chatroom_name':m.chatroom.name,
            'text':m.text
        } for m in messages
    ]
    sort_by = request.args.get('sort')
    if sort_by:
        messages_list.sort(key=lambda x: x[sort_by])
    return render_template('user_message_dashboard.html',
            title='NinerChat | User Messages',
            template='user-message-dashboard',
            current_user=current_user,
            user=user,
            messages=messages_list,
            body="{} Messages Dashboard".format(user.username))
        

@dashboard_bp.route('/users/<id>/change')
@admin_only
def change_admin(id):
    """ Toggle user admin True/False """
    user = User.query.filter_by(id=int(id)).first()
    if user.email != 'ninerchat@uncc.edu':
        user.admin = not user.admin
        db.session.commit()
    else:
        flash('Ninerchat admin can not be changed')
    return redirect(url_for('dashboard_bp.user_profile', id = user.id))

@dashboard_bp.route('/rooms')
@admin_only
def room():
    """ Room dashboard """
    return render_template('room_dashboard.html',
        title='NinerChat | Room Dashboard',
        template='room-dashboard',
        current_user=current_user,
        body="Room Dashboard")

@dashboard_bp.route('/reports')
@admin_only
def report():
    """ Report dashboard """
    return render_template('report_dashboard.html',
        title='NinerChat | Report Dashboard',
        template='report-dashboard',
        current_user=current_user,
        body="Report Dashboard")

