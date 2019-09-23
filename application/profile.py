"""Routes for user user profiles."""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash
from .forms import ProfileForm
from .models import db, User
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
        oldpassword = request.form.get('oldpassword')
        if current_user.check_password(password=oldpassword):
            name = request.form.get('name')
            password = request.form.get('password')
            current_user.username = name
            current_user.set_password(password)
            db.session.commit()
            flash('Profile Updated')
        else:
            flash('Unable to update: old password incorrect')
            return redirect(url_for('profile_bp.update_profile'))
        return redirect(url_for('profile_bp.profile'))
    elif request.method == 'GET':
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
