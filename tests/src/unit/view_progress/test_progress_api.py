from http import HTTPStatus

import pytest

from src.app import app
from tests.fake.services import FakeViewProgressRepository


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {
                "film_id": "e6a60937-fb0d-44d4-81f3-15d2170f1fe2",
                "viewed_frame": 234,
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
                "film_id": "e6a60937-fb0d-44d4-81f3-15d2170f1fe2",
                "viewed_frame": "234",
            },
            {
                "status_code": HTTPStatus.UNPROCESSABLE_ENTITY,
                "analyse_data": False,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_post_frame(input, expected, test_app_client):
    with app.container.user_view_history_service.override(
        FakeViewProgressRepository()
    ):
        response = test_app_client.post(
            "api/v1/view_progress",
            json=input,
        )

    assert response.status_code == expected["status_code"]

    if expected["analyse_data"]:
        data = response.json()
        assert data[expected["key"]] == expected["response"]


@pytest.mark.asyncio
async def test_get_frame(test_app_client):
    film_id = "e6a60937-fb0d-44d4-81f3-15d2170f1fe2"

    with app.container.user_view_history_service.override(
        FakeViewProgressRepository()
    ):
        response = test_app_client.get(
            f"api/v1/view_progress?film_id={film_id}"
        )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["film_id"] == film_id
    assert data.get("viewed_frame") == 123
