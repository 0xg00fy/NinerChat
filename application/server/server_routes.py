"""Routes for the ninerchat server"""
from flask import Blueprint, render_template
from flask import current_app as app

# Blueprints
server_bp = Blueprint('server_bp', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/server')

@server_bp.route('/users', methods=['GET'])
def users():
    """List users route"""
    return render_template('users.html',
        title='NinerChat | User List'
        template='users-template')
