from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    # Application configuration
    app.config.from_object('config.Config')

    # Plugins
    db.init_app(app)

    with app.app_context():
        # import parts of app
        from .client import client_routes
        from .server import server_routes

        # register Blueprints
        app.register_blueprint(client_routes.client_bp)
        app.register_blueprint(server_routes.server_bp)

        return app
