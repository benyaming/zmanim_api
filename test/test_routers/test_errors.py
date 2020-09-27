import pytest
from fastapi.testclient import TestClient

from zmanim_api.main import app


client = TestClient(app)


@pytest.mark.api
@pytest.mark.error
def test_daf_yomi_endpoint():
    params = {'date': 'broken_date'}
    expected = {'message': 'Invalid date provided! Invalid isoformat string: \'broken_date\''}

    actual = client.get('/daf_yomi', params=params)
    assert actual.status_code == 400
    assert actual.json() == expected
