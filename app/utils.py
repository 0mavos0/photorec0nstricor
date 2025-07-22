import re
import os


def sanitize_input(input_str):
    return re.sub(r'[^a-zA-Z0-9_\-\./]', '', input_str)


def is_valid_drive_path(path):
    return os.path.exists(path)


def list_drives():
    return [f"/dev/{d}" for d in os.listdir("/dev") if d.startswith("sd")]
