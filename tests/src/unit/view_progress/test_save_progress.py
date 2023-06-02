from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.brokers.exceptions import ProducerError
from src.services.user_view_history import UserViewHistoryService
from tests.fake.services import FakeProducer, FakeUARepository


@pytest.mark.asyncio
async def test_ua_service_save_progress(frame_data):
    service = UserViewHistoryService(FakeProducer(), FakeUARepository())

    await service.send_view_progress(frame_data)


@pytest.mark.parametrize(
    "key_to_remove",
    [
        "user_id",
        "film_id",
        "viewed_frame",
    ],
)
@pytest.mark.asyncio
async def test_ua_service_save_progress_missing_parameters(
    frame_data, key_to_remove
):
    service = UserViewHistoryService(FakeProducer(), FakeUARepository())

    local_data = frame_data.copy()
    local_data.pop(key_to_remove)

    with pytest.raises(HTTPException) as e_info:
        await service.send_view_progress(local_data)

    assert e_info.value.status_code == HTTPStatus.BAD_REQUEST


async def throw_error(*args, **kwargs):
    raise ProducerError("some error")


@pytest.mark.asyncio
async def test_ua_service_save_progress_send_failed(frame_data):
    producer = FakeProducer()
    producer.send = throw_error

    service = UserViewHistoryService(producer, FakeUARepository())

    with pytest.raises(HTTPException) as e_info:
        await service.send_view_progress(frame_data)

    assert e_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
