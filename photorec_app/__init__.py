import os
from flask import Flask
from flask_cors import CORS
from flask_redis import FlaskRedis
from flask_socketio import SocketIO


def create_app(config_object='config.Config'):
    """Application factory to create Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_object)
    CORS(app)

    app.config.setdefault('REDIS_URL', 'redis://localhost:6379/0')
    FlaskRedis(app)

    SocketIO(app, cors_allowed_origins="*")

    try:
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)
    except Exception:
        # Blueprint may be missing in dummy setup
        pass

    return app
