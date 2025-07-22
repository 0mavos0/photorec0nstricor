import re
import shlex


def sanitize_input(input_str: str) -> str:
    """Sanitize strings to avoid shell injection."""
    return shlex.quote(input_str)


def is_valid_drive_path(drive_path: str) -> bool:
    """Validate that the drive path resembles a /dev/ entry."""
    return bool(re.match(r"^/dev/[a-zA-Z0-9]+$", drive_path))

import os


def sanitize_input(input_str):
    return re.sub(r'[^a-zA-Z0-9_\-\./]', '', input_str)


def is_valid_drive_path(path):
    return os.path.exists(path)


def list_drives():
    return [f"/dev/{d}" for d in os.listdir("/dev") if d.startswith("sd")]

