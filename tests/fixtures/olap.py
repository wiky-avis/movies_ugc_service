import clickhouse_connect
import pytest

from src.settings.db import OlapSettings


@pytest.fixture(scope="session")
def db_settings():
    settings = OlapSettings()
    return settings


@pytest.fixture(scope="session")
def olap_client(db_settings):
    client = clickhouse_connect.get_client(
        host=db_settings.host,
        port=db_settings.port,
        username=db_settings.username,
    )

    client.command("truncate table if exists ugc.user_progress")

    yield client

    client.command("truncate table if exists ugc.user_progress")
