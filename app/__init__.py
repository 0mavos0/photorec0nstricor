from flask import Flask
from flask_redis import FlaskRedis
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['REDIS_URL'] = "redis://redis:6379/0"
redis_client = FlaskRedis(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Import routes after app creation
from app import routes  # noqa: E402

