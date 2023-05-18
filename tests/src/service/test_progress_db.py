from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.services.user_activity_service import UserActivityService
from tests.fake.services import FakeProducer, FakeUARepository


@pytest.mark.asyncio
async def test_ua_service_db_insert_value(frame_data):
    producer = FakeProducer()
    repository = FakeUARepository()
    service = UserActivityService(producer, repository)

    await service.insert_or_update_view_progress(frame_data)

    stored = await repository.find_one(
        dict(film_id=frame_data["film_id"], user_id=frame_data["user_id"]),
        "table",
    )

    assert stored.get("viewed_frame") is not None


@pytest.mark.asyncio
async def test_ua_service_db_update_value(frame_data):
    producer = FakeProducer()
    repository = FakeUARepository()
    service = UserActivityService(producer, repository)

    # Первый фрейм
    frame_1 = frame_data.copy()
    frame_1["viewed_frame"] = 1

    await service.insert_or_update_view_progress(frame_1)

    # Второй фрейм
    frame_2 = frame_data.copy()
    frame_2["viewed_frame"] = 2

    await service.insert_or_update_view_progress(frame_2)

    stored = await repository.find_one(
        dict(film_id=frame_data["film_id"], user_id=frame_data["user_id"]),
        "table",
    )

    assert stored.get("viewed_frame") == 2


@pytest.mark.parametrize(
    "key_to_remove",
    [
        ("user_id"),
        ("film_id"),
        ("viewed_frame"),
    ],
)
@pytest.mark.asyncio
async def test_ua_service_db_insert_value_missing_parameters(
    frame_data, key_to_remove
):
    service = UserActivityService(FakeProducer(), FakeUARepository())

    local_data = frame_data.copy()
    local_data.pop(key_to_remove)

    with pytest.raises(HTTPException) as e_info:
        await service.send_view_progress(local_data)

    assert e_info.value.status_code == HTTPStatus.BAD_REQUEST
