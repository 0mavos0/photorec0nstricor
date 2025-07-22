from flask import Blueprint, jsonify, request

from .recovery import load_settings, start_recovery_process
from .utils import sanitize_input, is_valid_drive_path, list_drives

main = Blueprint('main', __name__)


@main.route('/drives', methods=['GET'])
def get_drives():
    """Return available drive paths."""
    return jsonify(list_drives())


@main.route('/start_recovery', methods=['POST'])
def start_recovery():
    data = request.get_json() or {}
    drive_path = sanitize_input(data.get('drive_path', ''))
    if drive_path and not is_valid_drive_path(drive_path):
        return jsonify({'error': 'Invalid drive path'}), 400

    settings = load_settings()
    start_recovery_process(settings)
    return jsonify({'message': 'Recovery process started'}), 202
