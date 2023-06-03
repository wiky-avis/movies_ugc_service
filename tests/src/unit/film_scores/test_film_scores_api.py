import json
from http import HTTPStatus

import pytest

from src.app import app
from tests.fake.services import FakeFilmScoresRepository


film_id = "4e0cff77-496e-4cd7-9c93-8ce6477333cd"


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            {
                "film_id": film_id,
                "score": 9,
            },
            {
                "status_code": HTTPStatus.OK,
                "analyse_data": True,
                "key": "result",
                "response": "Ok.",
            },
        ),
        (
            {
                "film_id": film_id,
                "score": 11,
            },
            {
                "status_code": HTTPStatus.UNPROCESSABLE_ENTITY,
                "analyse_data": False,
            },
        ),
        (
            {
                "film_id": film_id,
                "score": 0,
            },
            {
                "status_code": HTTPStatus.UNPROCESSABLE_ENTITY,
                "analyse_data": False,
            },
        ),
        (
            {
                "film_id": film_id,
                "score": "9",
            },
            {
                "status_code": HTTPStatus.OK,
                "analyse_data": True,
                "key": "result",
                "response": "Ok.",
            },
        ),
        (
            {
                "film_id": film_id,
                "score": 8.5,
            },
            {
                "status_code": HTTPStatus.OK,
                "analyse_data": True,
                "key": "result",
                "response": "Ok.",
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_post_score(test_input, expected, test_app_client):
    with app.container.user_film_scores_service.override(
        FakeFilmScoresRepository()
    ):
        response = test_app_client.post(
            "api/v1/film_scores",
            json=test_input,
        )

    assert response.status_code == expected["status_code"]

    if expected["analyse_data"]:
        data = response.json()
        assert data[expected["key"]] == expected["response"]


@pytest.mark.asyncio
async def test_delete_score(test_app_client):
    with app.container.user_film_scores_service.override(
        FakeFilmScoresRepository()
    ):
        response = test_app_client.delete(
            "api/v1/film_scores",
            json={"film_id": film_id},
        )

    assert response.status_code == HTTPStatus.NO_CONTENT

    response_text = response.json()
    assert response_text == "Score successfully deleted"


@pytest.mark.asyncio
async def test_get_score(test_app_client):
    with app.container.user_film_scores_service.override(
        FakeFilmScoresRepository()
    ):
        response = test_app_client.get(
            f"api/v1/film_scores?film_id={film_id}",
        )

    assert response.status_code == HTTPStatus.OK

    response_body = response.json()
    response_content = json.loads(response_body)

    assert response_content["film_id"] == film_id
    assert type(response_content["score"]) == int


@pytest.mark.filterwarnings(
    "ignore"
)  # Игнорируется ворнинг FastAPIPaginationWarning.
# Он навязывает использование fastapi_pagination.ext.motor.paginate вместо простого paginate
@pytest.mark.asyncio
async def test_get_top_scores(test_app_client):
    with app.container.user_film_scores_service.override(
        FakeFilmScoresRepository()
    ):
        response1 = test_app_client.get(
            "api/v1/film_scores/top?page=1&size=10"
        )

    assert response1.status_code == HTTPStatus.OK

    response_body = response1.json()
    response_content = response_body["items"]

    assert type(response_content) == list

    for item in response_content:
        assert item.get("film_id") is not None
        assert item.get("avg_score") is not None
        assert item.get("num_scores") is not None
