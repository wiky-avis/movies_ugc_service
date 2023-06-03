import pytest

from src.services.user_view_history import UserViewHistoryService
from tests.fake.services import FakeProducer, FakeUARepository


@pytest.mark.asyncio
async def test_ua_service_db_insert_value(frame_data):
    producer = FakeProducer()
    repository = FakeUARepository()
    service = UserViewHistoryService(producer, repository)

    await service.insert_or_update_view_progress(frame_data)

    stored = await repository.find_one(
        dict(film_id=frame_data.film_id, user_id=frame_data.user_id),
        "view_progress",
    )

    assert stored.get("viewed_frame") == frame_data.viewed_frame


@pytest.mark.asyncio
async def test_ua_service_db_update_value(frame_data):
    producer = FakeProducer()
    repository = FakeUARepository()
    service = UserViewHistoryService(producer, repository)

    # Первый фрейм
    frame_data.viewed_frame = 1
    await service.insert_or_update_view_progress(frame_data)

    # Второй фрейм
    frame_data.viewed_frame = 2
    await service.insert_or_update_view_progress(frame_data)

    stored = await repository.find_one(
        dict(film_id=frame_data.film_id, user_id=frame_data.user_id),
        "view_progress",
    )

    assert stored.get("viewed_frame") == 2
