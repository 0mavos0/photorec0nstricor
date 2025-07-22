from flask import Blueprint, jsonify, request

# Blueprint for API routes
main = Blueprint('main', __name__)


def list_drives():
    """Dummy implementation returning example drives."""
    return ['/dev/sda', '/dev/sdb']


def sanitize_input(value: str) -> str:
    """Very basic sanitization removing suspicious characters."""
    import re
    return re.sub(r'[^a-zA-Z0-9_\-./]', '', value)


def is_valid_drive_path(path: str) -> bool:
    """Check if a drive path is plausible."""
    return path.startswith('/dev/')


@main.route('/drives', methods=['GET'])
def get_drives():
    return jsonify(list_drives())


@main.route('/start_recovery', methods=['POST'])
def start_recovery():
    data = request.get_json() or {}
    drive_path = sanitize_input(data.get('drive_path', ''))
    if not is_valid_drive_path(drive_path):
        return jsonify({'error': 'Invalid drive path'}), 400
    return jsonify({'message': 'Recovery process started'}), 202
