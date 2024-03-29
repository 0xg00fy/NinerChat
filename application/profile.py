"""Routes for user user profiles."""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash
from application.forms import ProfileForm
from application.models import db, User, Chatroom
from application.room import remove_member, add_member, add_room
from application import college_majors
from . import login_manager

# Blueprint Configuration
profile_bp = Blueprint('profile_bp', __name__,
    template_folder='templates',
    static_folder='static')

@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """Show profile"""
    return render_template('profile.html',
        user=current_user,
        template='profile-page',
        body='Profile')

@profile_bp.route('/profile/update', methods=['GET','POST'])
@login_required
def update_profile():
    """Update profile"""
    profile_form = ProfileForm(request.form)
    if request.method == 'POST' and profile_form.validate():
        # check that old password is correct
        oldpassword = request.form.get('oldpassword')
        if current_user.check_password(password=oldpassword):
            
            # get data from signup form
            name = request.form.get('name')
            password = request.form.get('password')
            major_id = request.form.get('major')
            college, major = college_majors.get(major_id)
            
            # remove user from colege major rooms
            college_room = Chatroom.query.filter_by(
                name=current_user.college
                ).first()
            major_room = Chatroom.query.filter_by(
                name=current_user.major
                ).first()
            for room in [college_room,major_room]:
                remove_member(current_user,room)
            
            # update current user info
            current_user.username = name
            current_user.set_password(password)
            current_user.college = college
            current_user.major = major

            # add user to rooms
            for item in [college,major]:
                add_room(item)
                room = Chatroom.query.filter_by(name=item).first()
                add_member(current_user,room)
            
            # commit changes to database
            db.session.commit()
            flash('Profile Updated')
        else:
            # old passwaord is incorrect
            flash('Unable to update: old password incorrect')
            return redirect(url_for('profile_bp.update_profile'))
        return redirect(url_for('profile_bp.profile'))
    elif request.method == 'GET':
        # Serve the update profile form
        return render_template('update_profile.html',
            form=ProfileForm(),
            user=current_user,
            title='NinerChat | Update Profile',
            template='profile-update',
            body="Update your profile")
    else:
        for field, errors in profile_form.errors.items():
            flash(u'%s - %s' % (profile_form[field].label.text, ','.join(errors)))
        return redirect(url_for('profile_bp.update_profile'))
