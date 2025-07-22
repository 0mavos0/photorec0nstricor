from flask import request, jsonify
from ..utils.sanitization import sanitize_input, is_valid_drive_path

@app.route('/start_recovery', methods=['POST'])
def start_recovery():
    data = request.get_json()
    drive_path = sanitize_input(data.get('drive_path', ''))
    if not is_valid_drive_path(drive_path):
        return jsonify({'error': 'Invalid drive path'}), 400
    # Proceed with the recovery process
    return jsonify({'message': 'Recovery process started'}), 202
