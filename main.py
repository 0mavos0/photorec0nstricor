from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import subprocess
import shlex
from threading import Thread
import redis
import json
from pexpect import spawn
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def sanitize_input(input_str):
    return re.sub(r'[^a-zA-Z0-9_\-\./]', '', input_str)


@socketio.on('connect', namespace='/recovery')
def test_connect():
    emit('response', {'message': 'Connected to recovery status updates'})


def start_photorec(drive_path):
    command = f"photorec {shlex.quote(drive_path)}"
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def emit_output(process):
        for line in process.stdout:
            socketio.emit('recovery_update', {'data': line}, namespace='/recovery')
        process.wait()
        socketio.emit('recovery_update', {'data': 'Recovery process completed'}, namespace='/recovery')

    thread = Thread(target=emit_output, args=(process,))
    thread.start()
    return "Photorec recovery process started."


@app.route('/api/start_recovery', methods=['POST'])
def api_start_recovery():
    settings_str = redis_client.get('recovery_options')
    if settings_str is None:
        return jsonify({'message': "Recovery settings not found."}), 404
    settings = json.loads(settings_str)
    recovery_path = sanitize_input(settings.get('recovery_path', ''))
    drive = sanitize_input(settings.get('drive', ''))
    message = start_photorec(drive_path=drive)
    return jsonify({'message': message}), 202


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
