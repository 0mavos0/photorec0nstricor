A lightweight Flask API wrapping [PhotoRec](https://www.cgsecurity.org/). It exposes endpoints to list available drives and to start a recovery process. Progress messages are streamed to connected clients via Socket.IO.

This project provides a simple Flask interface around PhotoRec to allow
starting recovery jobs and streaming their progress via SocketIO.


## Usage

### Docker

```bash
docker-compose up --build
```

### Local

```bash
pip install -r requirements.txt
python -m app.main
```

## Node WebSocket Server

A simple Node.js server using Express and `ws` serves the React frontend and forwards commands to a Docker container. Install the dependencies and run:

```bash
npm install
npm start
```
The recovery process can be started by POSTing to `/start_recovery`.
The endpoint expects a JSON body with a `drive_path` field pointing to a valid
`/dev` device.

