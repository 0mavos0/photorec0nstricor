from flask import Flask
from flask_redis import FlaskRedis
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['REDIS_URL'] = "redis://redis:6379/0"
redis_client = FlaskRedis(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Import routes after app creation
from app import routes  # noqa: E402
from flask_cors import CORS
from flask_redis import FlaskRedis
from flask_socketio import SocketIO


def create_app(config_filename='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    CORS(app)
    app.config['REDIS_URL'] = "redis://localhost:6379/0"
    redis_client = FlaskRedis(app)
    socketio = SocketIO(app, cors_allowed_origins="*")
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

