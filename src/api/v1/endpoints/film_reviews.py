import uuid
from http import HTTPStatus

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page

from src.api.v1.models.film_reviews import Review, ReviewList
from src.api.v1.models.responses import (
    AddFilmReviewResponse,
    InternalServerError,
    NotFound,
)
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.user_film_reviews import UserFilmReviewsService


router = APIRouter()


@router.get(
    "/film/{film_id}/reviews",
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="Получить список рецензий к фильму.",
    description="Получить список рецензий к фильму, отсортированный по дате создания.",
)
@inject
async def get_film_reviews(
    film_id: str,
    user_film_reviews_service: UserFilmReviewsService = Depends(
        Provide[Container.user_film_reviews_service]
    ),
    user_data=Depends(get_decoded_data),
) -> Page[ReviewList]:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await user_film_reviews_service.get_film_reviews(
        film_id=film_id  # type: ignore[arg-type]
    )


@router.post(
    "/film/{film_id}/reviews",
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="Оставить рецензию к фильму.",
    description="Добавление пользователем рецензии к фильму.",
)
@inject
async def add_film_review(
    film_id: str,
    review_title: str,
    review_body: str,
    user_film_reviews_service: UserFilmReviewsService = Depends(
        Provide[Container.user_film_reviews_service]
    ),
    user_data=Depends(get_decoded_data),
) -> AddFilmReviewResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    user_film_review = dict(
        user_id=user_id,
        film_id=film_id,
        review_id=str(uuid.uuid4()),
        review_title=review_title,
        review_body=review_body,
    )

    await user_film_reviews_service.create_film_review(user_film_review)

    return await user_film_reviews_service.send_film_review(user_film_review)


@router.get(
    "/reviews/{review_id}",
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="Получить рецензию к фильму.",
    description="Получение пользовательской рецензии к фильму.",
)
@inject
async def get_film_review(
    review_id: str,
    user_film_reviews_service: UserFilmReviewsService = Depends(
        Provide[Container.user_film_reviews_service]
    ),
    user_data=Depends(get_decoded_data),
) -> Review:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await user_film_reviews_service.get_film_review(
        review_id=review_id  # type: ignore[arg-type]
    )
