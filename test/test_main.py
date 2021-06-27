from fastapi.testclient import TestClient

from zmanim_api.main import app

client = TestClient(app)


def test_swagger():
    resp = client.get('/')
    assert resp.status_code == 200

