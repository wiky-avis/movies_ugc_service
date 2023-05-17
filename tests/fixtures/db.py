import clickhouse_connect
import pytest

from src.settings.db import DBSettings


@pytest.fixture(scope="session")
def db_settings():
    settings = DBSettings()
    return settings


@pytest.fixture(scope="session")
def db_client(db_settings):
    client = clickhouse_connect.get_client(
        host=db_settings.host,
        port=db_settings.port,
        username=db_settings.username,
    )

    yield client
