import aiohttp
import pytest_asyncio

from src.settings import auth_settings


@pytest_asyncio.fixture(scope="session")
async def aiohttp_session(get_encoded_token):
    cookies = dict()
    cookies[auth_settings.auth_secure_key] = get_encoded_token

    session = aiohttp.ClientSession(cookies=cookies)

    yield session
    await session.close()
