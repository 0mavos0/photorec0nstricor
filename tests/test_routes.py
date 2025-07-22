import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_drives(client, monkeypatch):
    monkeypatch.setattr('app.routes.list_drives', lambda: ['/dev/sda'])
    resp = client.get('/drives')
    assert resp.status_code == 200
    assert resp.get_json() == ['/dev/sda']


def test_start_recovery_success(client, monkeypatch):
    monkeypatch.setattr('app.routes.is_valid_drive_path', lambda p: True)
    monkeypatch.setattr('app.routes.load_settings', lambda: object())
    called = {}
    def fake_start(_):
        called['called'] = True
    monkeypatch.setattr('app.routes.start_recovery_process', fake_start)
    resp = client.post('/start_recovery', json={'drive_path': '/dev/sda'})
    assert resp.status_code == 202
    assert called.get('called')


def test_start_recovery_invalid_drive(client, monkeypatch):
    monkeypatch.setattr('app.routes.is_valid_drive_path', lambda p: False)
    resp = client.post('/start_recovery', json={'drive_path': '/dev/invalid'})
    assert resp.status_code == 400
