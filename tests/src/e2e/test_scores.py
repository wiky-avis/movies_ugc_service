import json
from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_film_score_post_request(aiohttp_session, user_settings):
    # Отправляем через API просмотренный фрейм
    film_id = "dc3825a9-8668-400e-b083-97aa24081352"
    host = f"http://127.0.0.1:8000/api/v1/score-film/{film_id}"
    body = {"score": 9}
    async with aiohttp_session.post(host, json=body) as resp:
        assert resp.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_film_score_get_request(aiohttp_session, user_settings):
    # Отправляем через API просмотренный фрейм
    film_id = "b18d7b24-f2db-4f2a-b584-55da3cad8b26"
    host = f"http://127.0.0.1:8000/api/v1/score-film/{film_id}"
    user_id = user_settings["user_id"]
    body = {"score": 9}
    async with aiohttp_session.post(host, json=body) as resp:
        assert resp.status == HTTPStatus.OK

    # Ходим с теми же параметрами, но только делаем get request
    async with aiohttp_session.get(host) as resp:
        assert resp.status == HTTPStatus.OK
        result_str = await resp.json()

    api_result = json.loads(result_str)

    # Ожидаем ровно не же параметры, которые передали
    assert api_result.get("film_id") == film_id
    assert api_result.get("user_id") == user_id
    assert api_result.get("score") == body["score"]


@pytest.mark.asyncio
async def test_film_score_delete_request(aiohttp_session, user_settings):
    # Отправляем через API просмотренный фрейм
    film_id = "39e7114a-f61e-461d-b2b4-9c5037b5051b"
    host = f"http://127.0.0.1:8000/api/v1/score-film/{film_id}"
    body = {"score": 9}
    async with aiohttp_session.post(host, json=body) as resp:
        assert resp.status == HTTPStatus.OK

    # Удаляем этот же фильм
    async with aiohttp_session.delete(host) as resp:
        assert resp.status == HTTPStatus.OK

    # Если фильма нет, то отдает код 404
    async with aiohttp_session.get(host) as resp:
        assert resp.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_film_score_top_films(aiohttp_session, user_settings):
    # Отправляем через API просмотренный фрейм
    film_ids = [
        "8175e978-aa59-4171-ab1c-f416f65e4c74",
        "8222682e-7cc7-41fc-9ac8-c6ecc58e493d",
        "b07f6584-db4c-4f3f-b343-b635d52b1d40",
    ]
    api_host = "http://127.0.0.1:8000"
    post_score_path = "/api/v1/score-film/"
    post_body = {"score": 10}

    # Записываем фильмы с самой большой оценкой
    for film_id in film_ids:
        host = api_host + post_score_path + film_id
        async with aiohttp_session.post(host, json=post_body) as resp:
            assert resp.status == HTTPStatus.OK

    top_score_path = "/api/v1/top-films/by-score"
    top_body = {"limit": 30}

    # Запрашиваем топ фильмов
    async with aiohttp_session.get(
        api_host + top_score_path, json=top_body
    ) as resp:
        assert resp.status == HTTPStatus.OK
        api_result = await resp.json()

    # Распаковываем полученные фильмы и оставляем только id фильма
    top_films = {row["film_id"] for row in api_result}

    # Может содержать больше фильмов, чем указали, но переданные 3 точно должны быть
    for film in film_ids:
        assert film in top_films
