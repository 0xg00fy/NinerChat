"""Routes for the ninerchat server"""
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user
from flask import current_app as app
from .auth import admin_only
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
    # get public chatrooms
    public_chatrooms = Chatroom.query.filter_by(public=True).all()
    
    # get the memberlist entries for user, which should be private rooms
    memberlist = MemberList.query.filter_by(user_id=current_user.id).all()
    
    # get the chatroom from memberlist's chatroom database relationship
    # see models.py for the exact relationship used to perform this
    private_chatrooms = [item.chatroom for item in memberlist]
    
    return render_template('client.html',
        title='NinerChat | Welcome',
        template='client-template',
        current_user=current_user,
        public_chatrooms=public_chatrooms,
        private_chatrooms=private_chatrooms,
        body="You are now logged in!")

@main_bp.route('/users', methods=['GET'])
@admin_only
def users():
    """List users route"""
    
    # get all users in database
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
    
    # add admin user
    admin_user = User(
        username='admin',
        email='ninerchat@uncc.edu',
        password='admin',
        admin=True)
    db.session.add(admin_user)
    db.session.commit()
    
    flash("Database refreshed")
    return redirect(url_for('main_bp.chat'))
