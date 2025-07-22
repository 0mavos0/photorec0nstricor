import re


def sanitize_input(value: str) -> str:
    """Remove potentially dangerous characters."""
    return re.sub(r'[^a-zA-Z0-9_\-./]', '', value)


def is_valid_drive_path(path: str) -> bool:
    return path.startswith('/dev/')


def list_drives():
    """Return a list of dummy drive paths."""
    return ['/dev/sda', '/dev/sdb']
