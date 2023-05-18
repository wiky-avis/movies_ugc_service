import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.common.decode_auth_token import get_decoded_data
from tests.fake.jwt import fake_decode_token


@pytest.fixture(scope="session")
def test_app_client():
    app.dependency_overrides[get_decoded_data] = fake_decode_token

    client = TestClient(app)
    return client
