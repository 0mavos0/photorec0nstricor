import configparser
import logging
import os
import signal
import time
from dataclasses import dataclass
from threading import Thread

import pexpect

from app import socketio


@dataclass
class RecoverySettings:
    recovery_directory: str
    photorec_executable: str
    session_file: str
    file_count_threshold: int
    size_threshold_bytes: int
    minimum_file_size_bytes: int


def load_settings(config_path: str = 'settings.ini') -> RecoverySettings:
    config = configparser.ConfigParser()
    config.read(config_path)
    section = config['Settings']
    return RecoverySettings(
        recovery_directory=section.get('recovery_directory', '/tmp/recovered'),
        photorec_executable=section.get('photorec_executable', 'photorec'),
        session_file=section.get('photorec_ses_path', ''),
        file_count_threshold=section.getint('file_count_threshold', 100),
        size_threshold_bytes=section.getint('size_threshold_bytes', 0),
        minimum_file_size_bytes=section.getint('minimum_file_size_bytes', 0),
    )


def _filter_small_files(directory: str, min_size: int) -> None:
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path) and os.path.getsize(path) < min_size:
            os.remove(path)
            logging.info("Deleted %s: size below threshold", name)


def _monitor_directory(settings: RecoverySettings, process: pexpect.spawn) -> None:
    while process.isalive():
        files = [f for f in os.listdir(settings.recovery_directory)
                 if os.path.isfile(os.path.join(settings.recovery_directory, f))]
        if len(files) >= settings.file_count_threshold:
            logging.info("File threshold reached; pausing PhotoRec")
            os.kill(process.pid, signal.SIGSTOP)
            _filter_small_files(settings.recovery_directory, settings.size_threshold_bytes)
            os.kill(process.pid, signal.SIGCONT)
            logging.info("Resumed PhotoRec")
        time.sleep(5)


def start_recovery_process(settings: RecoverySettings) -> None:
    """Start PhotoRec with monitoring in a background thread."""

    def recovery_task():
        child = pexpect.spawn(
            f"{settings.photorec_executable}", encoding='utf-8'
        )
        child.expect("PhotoRec .* to continue", timeout=120)
        child.sendline("Y")
        socketio.emit('recovery_update', {'data': 'PhotoRec started'}, namespace='/recovery')

        monitor = Thread(target=_monitor_directory, args=(settings, child), daemon=True)
        monitor.start()

        while True:
            try:
                line = child.readline()
            except pexpect.EOF:
                break
            if line:
                socketio.emit('recovery_update', {'data': line.strip()}, namespace='/recovery')
        socketio.emit('recovery_update', {'data': 'Recovery process completed'}, namespace='/recovery')

    Thread(target=recovery_task, daemon=True).start()
