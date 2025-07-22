import re
import os


def sanitize_input(input_str):
    """Sanitize inputs to prevent command injection."""
    return re.sub(r'[^a-zA-Z0-9_\-\./]', '', input_str)


def is_valid_drive_path(drive_path):
    """Validate drive paths. Implement specific logic as needed."""
    return re.match(r'^/dev/sd[a-z]$', drive_path) is not None


def validate_path(path, path_type):
    """Validate and sanitize paths."""
    sanitized_path = sanitize_input(path)
    if path_type == "directory" and not os.path.isdir(sanitized_path):
        return False, None
    elif path_type == "file" and not os.path.isfile(sanitized_path):
        return False, None
    return True, sanitized_path


def validate_numeric_input(input_str):
    try:
        val = int(input_str)
        return True, val
    except ValueError:
        return False, 0
