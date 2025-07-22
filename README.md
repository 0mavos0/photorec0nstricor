# photorec0nstricor

A lightweight Flask API wrapping [PhotoRec](https://www.cgsecurity.org/). It exposes endpoints to list available drives and to start a recovery process. Progress messages are streamed to connected clients via Socket.IO.

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

The recovery process can be started by POSTing to `/start_recovery`.
