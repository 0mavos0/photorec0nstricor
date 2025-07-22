from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('connect', namespace='/recovery')
def test_connect():
    emit('response', {'message': 'Connected to recovery status updates'})
