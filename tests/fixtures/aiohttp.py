import pytest
import pytest_asyncio
import aiohttp
import uuid


@pytest_asyncio.fixture(scope="session")
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
