import sys


sys.path.insert(0, "/Users/vnikisov/YandexPraktikum/movies_ugc_service")


pytest_plugins = (
    "fixtures.asyncio",
    "fixtures.aiohttp",
    "fixtures.events",
    "fixtures.olap",
    "fixtures.jwt",
    "fixtures.api",
)
