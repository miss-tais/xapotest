from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import app_config

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=False)


def create_app(config_name):
    """Create and configure an instance of the Flask application."""

    app.config.from_object(app_config[config_name])

    from app.urls import api_bp
    app.register_blueprint(api_bp)

    db.init_app(app)

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app
