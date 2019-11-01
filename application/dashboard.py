"""Dashboard for the ninerchat server"""
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user
from flask import current_app as app
from application.auth import admin_only
from application.models import db, User, Chatroom, MemberList
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
    return render_template('user_dashboard.html',
        title='NinerChat | User Dashboard',
        template='user-dashboard',
        current_user=current_user,
        body="User Dashboard")

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

