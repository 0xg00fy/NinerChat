"""Routes for user authentication."""

from functools import wraps
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash
from application.forms import LoginForm, SignupForm
from application.models import db, User, Chatroom, MemberList
from application.room import add_member,add_room
from application import college_majors
from . import login_manager


# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
    template_folder='templates',
    static_folder='static')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """User login page."""
    # Bypass Login screen if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.chat'))
    login_form = LoginForm(request.form)
    # POST: Create user and redirect them to the app
    if request.method == 'POST':
        if login_form.validate():
            # Get Form Fields
            email = request.form.get('email')
            password = request.form.get('password')
            # Validate Login Attempt
            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password=password):
                    login_user(user)
                    next = request.args.get('next')
                    return redirect(next or url_for('main_bp.chat'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login_page'))
    # GET: Serve Log-in page
    return render_template('login.html',
                           form=LoginForm(),
                           title='NinerChat | Log in',
                           template='login-page',
                           body="Log in with your User account.")


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """User sign-up page."""
    signup_form = SignupForm(request.form)
    # POST: Sign user in
    if request.method == 'POST' and signup_form.validate():
        # Get Form Fields
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        major_id = request.form.get('major')
        college,major = college_majors.get(major_id)
        
        # Check if user is unique
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            user = User(username=name,
                        email=email,
                        password=password,
                        college=college,
                        major=major)
            db.session.add(user)
            db.session.commit()
            
            # login user
            login_user(user)
            user = current_user

            # add user to rooms
            for item in [college,major]:
                add_room(item)
                room = Chatroom.query.filter_by(name=item).first()
                add_member(user=user,room=room)
            return redirect(url_for('main_bp.chat'))
        else:
            flash('A user already exists with that email address.')
            return redirect(url_for('auth_bp.signup_page'))
    
    elif request.method == 'GET':
        # GET: Serve Sign-up page
        return render_template('/signup.html',
                           title='NinerChat | Create an Account',
                           form=SignupForm(),
                           template='signup-page',
                           body="Sign up for a user account.")
    else:
        for field, errors in signup_form.errors.items():
            flash(u'%s - %s' % (signup_form[field].label.text, ','.join(errors)))
        return redirect(url_for('auth_bp.signup_page'))


@auth_bp.route("/logout")
@login_required
def logout_page():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login_page'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login_page'))

# Decorator to allow only admin accounts to access
def admin_only(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated and current_user.admin:
            return func(*args, **kwargs)
        else:
            flash("That page is for admin users only!")
            return redirect(url_for('main_bp.chat'))
    return wrap

        

