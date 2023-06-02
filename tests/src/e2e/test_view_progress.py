import asyncio
import random
from ast import literal_eval
from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_view_progress_post_request(
    aiohttp_session, event_consumer, olap_client, user_settings
):
    # Отправляем черех API просмотренный фрейм
    film_id = "dc3825a9-8668-400e-b083-97aa24081352"
    host = f"http://fastapi:8000/api/v1/view_progress/{film_id}"
    user_id = user_settings["user_id"]
    body = {"viewed_frame": random.randint(1, 1000)}
    async with aiohttp_session.post(host, json=body) as resp:
        assert resp.status == HTTPStatus.OK

    # Подключаемся к кафке и смотрим, что там появилось событие
    event = await event_consumer.getone()
    event_value = literal_eval(event.value.decode("utf-8"))

    assert event_value["user_id"] == user_id
    assert event_value["film_id"] == film_id
    assert event_value["viewed_frame"] == body["viewed_frame"]

    # Ждем, пока прольется строка в таблицу
    await asyncio.sleep(5)

    # # Подключаемся к кликхаусу и смотрим, что там появилось событие
    result = olap_client.query(
        "SELECT user_id, film_id, viewed_frame FROM ugc.user_progress"
    )

    frames = set()

    for row in result.result_rows:
        olap_user_id = str(row[0])
        olap_film_id = str(row[1])
        olap_viewed_frame = row[2]

        if olap_user_id == user_id and olap_film_id == film_id:
            frames.add(olap_viewed_frame)

    assert body["viewed_frame"] in frames
