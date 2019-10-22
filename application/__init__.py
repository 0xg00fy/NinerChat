from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_object):
    app = Flask(__name__, instance_relative_config=False)

    # Application configuration
    app.config.from_object(config_object)

    # Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # import parts of app
        from . import auth, routes, profile, room

        # import API
        from .api import auth as api_auth
        from .api import profile as api_profile
        from .api import room as api_room

        # register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(profile.profile_bp)
        app.register_blueprint(room.room_bp)
        app.register_blueprint(api.api_bp)

        db.create_all()

        return app
