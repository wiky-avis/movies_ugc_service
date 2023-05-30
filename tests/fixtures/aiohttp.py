import aiohttp
import jwt
import pytest_asyncio

from src.settings import auth_settings
from tests.fake.request_id import fake_request_id


@pytest_asyncio.fixture(scope="session")
async def aiohttp_session(get_encoded_token):
    cookies = dict()
    cookies[auth_settings.auth_secure_key] = get_encoded_token

    session = aiohttp.ClientSession(cookies=cookies, headers=fake_request_id())

    yield session
    await session.close()


@pytest_asyncio.fixture(scope="session")
async def aiohttp_manual(get_encoded_token):
    token = jwt.encode(
        {"user_id": "1ff75749-a557-44e4-a99e-4cbe2ca77534"},
        "AUTH_SERVICE_SECRET_PUBLIC_KEY",
        algorithm="HS256",
    )

    cookies = dict()
    cookies["access_token_cookie"] = token

    session = aiohttp.ClientSession(cookies=cookies, headers=fake_request_id())

    yield session
    await session.close()
