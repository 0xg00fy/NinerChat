"""Routes for the ninerchat server"""
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user
from flask import current_app as app
from .models import db, User, Chatroom, MemberList
from .forms import ProfileForm
from flask_login import login_required

# Blueprints
main_bp = Blueprint('main_bp', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/')

@main_bp.route('/', methods=['GET'])
@login_required
def chat():
    """Serve the client"""
    public_chatrooms = Chatroom.query.filter_by(public=True).all()
    memberlist = MemberList.query.filter_by(user_id=current_user.id).all()
    private_chatrooms = [item.chatroom for item in memberlist]
    return render_template('client.html',
        title='NinerChat | Welcome',
        template='client-template',
        current_user=current_user,
        public_chatrooms=public_chatrooms,
        private_chatrooms=private_chatrooms,
        body="You are now logged in!")

@main_bp.route('/users', methods=['GET'])
def users():
    """List users route"""
    users = User.query.all()
    return render_template('users.html',
        title='NinerChat | User List',
        users = users,
        template='users-template')

@main_bp.route('/clear', methods=['GET'])
def clear():
    """Clear DB"""
    db.drop_all()
    db.create_all()
    return "Database refreshed"
