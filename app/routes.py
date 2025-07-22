from flask import Blueprint, request, jsonify
from .utils import sanitize_input, is_valid_drive_path, list_drives

main = Blueprint('main', __name__)

@main.route('/drives', methods=['GET'])
def get_drives():
    drives = list_drives()
    return jsonify(drives)

@main.route('/start_recovery', methods=['POST'])
def start_recovery():
    data = request.get_json()
    drive_path = sanitize_input(data.get('drive_path', ''))
    if not is_valid_drive_path(drive_path):
        return jsonify({'error': 'Invalid drive path'}), 400
    return jsonify({'message': 'Recovery process started'}), 202
