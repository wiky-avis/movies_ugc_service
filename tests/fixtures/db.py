import clickhouse_connect
import pytest

from src.settings.db import DBSettings


@pytest.fixture(scope="session")
def db_settings():
    return DBSettings()


@pytest.fixture(scope="session")
async def event_producer(db_settings):
    client = clickhouse_connect.get_client(
        host=db_settings.host,
        port=db_settings.port,
        username=db_settings.username,
        password=db_settings.password,
    )

    yield client
