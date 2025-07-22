This project provides a simple Flask interface around PhotoRec to allow
starting recovery jobs and streaming their progress via SocketIO.

## Usage

Run the application with Docker Compose:

```bash
docker-compose up --build
```
The API exposes an endpoint `/start_recovery` that expects a JSON body
with a `drive_path` field pointing to a valid `/dev` device.

# Photorec0nstricor

This project provides a simple Flask API for managing drive recovery using
`photorec`. The application exposes endpoints to list drives and start a
recovery process. Real-time status updates are sent over a WebSocket using
`flask_socketio`.

## Usage

Install the dependencies and run `main.py`:

```bash
pip install flask flask-cors flask-redis flask-socketio redis pexpect
python main.p

