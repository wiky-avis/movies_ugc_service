import pytest
import jwt

from src.settings import auth_settings


@pytest.fixture(scope="session")
def user_settings():
    settings = dict()
    settings['user_id'] = "1ff75749-a557-44e4-a99e-4cbe2ca77534"
    yield settings


@pytest.fixture(scope="session")
def get_encoded_token(user_settings):
    payload = dict()
    payload["user_id"] = user_settings['user_id']
    
    token = jwt.encode(payload, 
                       auth_settings.jwt_secret, 
                       algorithm=auth_settings.jwt_algorithm)
    
    yield token