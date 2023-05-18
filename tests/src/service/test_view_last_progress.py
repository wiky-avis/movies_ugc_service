from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.services.user_activity_service import UserActivityService
from tests.fake.services import FakeProducer, FakeUARepository


@pytest.mark.asyncio
async def test_last_view_progress(frame_data):
    producer = FakeProducer()
    repository = FakeUARepository()

    # Добавляем фейковые данные
    film_id = frame_data["film_id"]
    user_id = frame_data["user_id"]
    viewed_frame = frame_data["viewed_frame"]
    repository.storage[f"{film_id}:{user_id}"] = viewed_frame

    service = UserActivityService(producer, repository)

    filter_ = frame_data.copy()
    filter_.pop("viewed_frame")

    result = await service.get_last_view_progress(filter_)

    assert result.viewed_frame == viewed_frame


@pytest.mark.asyncio
async def test_last_view_progress_no_data(frame_data):
    producer = FakeProducer()
    repository = FakeUARepository()
    service = UserActivityService(producer, repository)

    filter_ = frame_data.copy()
    filter_.pop("viewed_frame")

    with pytest.raises(HTTPException) as e_info:
        await service.get_last_view_progress(filter_)

    assert e_info.value.status_code == HTTPStatus.NOT_FOUND
