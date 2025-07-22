A lightweight Flask API wrapping [PhotoRec](https://www.cgsecurity.org/). It exposes endpoints to list available drives and start a recovery process. Progress messages are streamed to connected clients via Socket.IO.

The project includes a minimal Node.js server which serves the React frontend and can forward WebSocket commands to a Docker container.

## Architecture

- **Flask API** (`app/`): Handles `/drives` and `/start_recovery`. When a recovery job runs, PhotoRec output is emitted on the `/recovery` Socket.IO namespace.
- **Node server** (`node_server.js`): Serves the built React files and exposes a WebSocket server on port `8080` for Docker commands.
- **Frontend** (`frontend/`): A React interface that selects a drive and displays live recovery logs from the Flask server.

## Running with Docker

1. Build and start the API (and Redis) using Docker Compose:

```bash
docker-compose up --build
```

2. In another terminal, install Node dependencies and start the server:

```bash
npm install
npm start
```

The Flask API listens on `http://localhost:5000`. The Node server hosts the frontend at `http://localhost:3000` and accepts WebSocket connections on `ws://localhost:8080`.

## Running locally without Docker

1. Install Python requirements and start the Flask API:

```bash
pip install -r requirements.txt
python -m app.main
```

## Node Socket.IO Server

A small Node.js server serves the React frontend and forwards commands to a
Docker container. Start it in another terminal:

```bash
npm install
npm start
```

The recovery process can be started by POSTing to `/start_recovery`. The
endpoint expects a JSON body with a `drive_path` field (e.g. `/dev/sda`).
WebSocket messages stream progress under the `/recovery` namespace.

Navigate to `http://localhost:3000` to use the frontend.

### API usage

Send a POST request to `/start_recovery` with JSON containing `drive_path` (e.g. `/dev/sda`):

```bash
curl -X POST http://localhost:5000/start_recovery \
     -H 'Content-Type: application/json' \
     -d '{"drive_path": "/dev/sda"}'
```

Progress updates will stream to connected clients under the `/recovery` namespace.
## Command line usage

Run the interactive CLI to start a recovery session:

```bash
python -m app.cli
```


## Running tests

Python tests are executed with `pytest`:

```bash
pip install -r requirements.txt
pytest
```

Node tests use `jest` and can be run with:

```bash
npm install
npm test
```


