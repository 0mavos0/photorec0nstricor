import re
import shlex


def sanitize_input(input_str: str) -> str:
    """Sanitize strings to avoid shell injection."""
    return shlex.quote(input_str)


def is_valid_drive_path(drive_path: str) -> bool:
    """Validate that the drive path resembles a /dev/ entry."""
    return bool(re.match(r"^/dev/[a-zA-Z0-9]+$", drive_path))
