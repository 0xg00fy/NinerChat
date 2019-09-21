"""Routes for the ninerchat client"""
from flask import Blueprint, render_template
from flask import current_app as app

# Blueprints
client_bp = Blueprint('client_bp', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/client')

@client_bp.route('/aboutme', methods=['GET'])
def users():
    """List user info"""
    return render_template('aboutme.html',
        title='NinerChat | About Me',
        template='aboutme-template')
