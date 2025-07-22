from flask import Flask
from flask_cors import CORS
from flask_redis import FlaskRedis
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")
redis_client = FlaskRedis()


def create_app(config_filename='config.Config'):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_filename)
    CORS(app)
    app.config.setdefault('REDIS_URL', 'redis://localhost:6379/0')
    redis_client.init_app(app)
    socketio.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
