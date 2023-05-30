import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.common.decode_auth_token import get_decoded_data
from tests.fake.jwt import fake_decode_token
from tests.fake.request_id import fake_request_id


@pytest.fixture(scope="session")
def test_app_client():
    app.dependency_overrides[get_decoded_data] = fake_decode_token

    client = TestClient(app, headers=fake_request_id())
    return client


@pytest.fixture()
def frame_data():
    frame_data = {
        "user_id": "15b6f6c7-ac87-4f67-9dc9-b8ee824e10bd",
        "film_id": "ae93cbdc-f147-41e1-b358-01aee63025aa",
        "viewed_frame": 1234,
    }
    return frame_data
