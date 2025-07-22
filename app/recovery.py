import subprocess
import shlex
from threading import Thread
from app import socketio


def emit_recovery_status(update: str) -> None:
    """Emit status updates via SocketIO."""
    socketio.emit('recovery_update', {'data': update}, namespace='/recovery')


def start_recovery_process(drive_path: str) -> None:
    """Run PhotoRec in a separate thread and stream updates."""

    def recovery_task():
        cmd = f"photorec /log /d /output {shlex.quote(drive_path)}"
        process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        if process.stdout:
            for line in process.stdout:
                emit_recovery_status(line.strip())

        emit_recovery_status('Recovery process completed')

    Thread(target=recovery_task, daemon=True).start()
