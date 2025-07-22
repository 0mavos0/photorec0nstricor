
# Photorec0nstricor

This project provides a simple Flask API for managing drive recovery using
`photorec`. The application exposes endpoints to list drives and start a
recovery process. Real-time status updates are sent over a WebSocket using
`flask_socketio`.

## Usage

Install the dependencies and run `main.py`:

```bash
pip install flask flask-cors flask-redis flask-socketio redis pexpect
python main.py
```

The API will listen on port `5000`.

