# photorec0nstricor

This project provides a simple Flask interface around PhotoRec to allow
starting recovery jobs and streaming their progress via SocketIO.

## Usage

Run the application with Docker Compose:

```bash
docker-compose up --build
```

The API exposes an endpoint `/start_recovery` that expects a JSON body
with a `drive_path` field pointing to a valid `/dev` device.

