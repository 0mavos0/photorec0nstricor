import os
import re
from typing import List, Tuple


def sanitize_input(input_str: str) -> str:
    """Remove potentially dangerous characters."""
    return re.sub(r'[^a-zA-Z0-9_\-./]', '', input_str)


def is_valid_drive_path(drive_path: str) -> bool:
    """Validate that the drive path resembles a block device."""
    return re.match(r'^/dev/sd[a-z]$', drive_path) is not None


def validate_path(path: str, path_type: str) -> Tuple[bool, str]:
    """Validate and sanitize a path."""
    sanitized = sanitize_input(path)
    if path_type == 'directory' and not os.path.isdir(sanitized):
        return False, ''
    if path_type == 'file' and not os.path.isfile(sanitized):
        return False, ''
    return True, sanitized


def validate_numeric_input(value: str) -> Tuple[bool, int]:
    try:
        return True, int(value)
    except (TypeError, ValueError):
        return False, 0


def list_drives() -> List[str]:
    return [f"/dev/{d}" for d in os.listdir('/dev') if d.startswith('sd')]
