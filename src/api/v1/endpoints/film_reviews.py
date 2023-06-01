import uuid
from http import HTTPStatus

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_pagination import Page

from src.api.v1.models.film_reviews import AddFilmReviewInput, ReviewList
from src.api.v1.models.responses import InternalServerError, NotFound
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.user_film_reviews import UserFilmReviewsService


router = APIRouter()


@router.get(
    "/reviews/{film_id}",
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="Получить список рецензий к фильму.",
    description="Получить список рецензий к фильму, отсортированный в порядке создания.",
)
@inject
async def get_film_reviews(
    film_id: str,
    user_film_reviews_service: UserFilmReviewsService = Depends(
        Provide[Container.user_film_reviews_service]
    ),
) -> Page[ReviewList]:
    return await user_film_reviews_service.get_film_reviews(film_id=film_id)


@router.post(
    "/reviews/{film_id}",
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="Оставить рецензию к фильму.",
    description="Добавление пользователем рецензии к фильму.",
)
@inject
async def add_film_review(
    film_id: str,
    review: AddFilmReviewInput = Body(...),
    user_film_reviews_service: UserFilmReviewsService = Depends(
        Provide[Container.user_film_reviews_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
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
        review_title=review.title,
        review_body=review.body,
    )

    await user_film_reviews_service.create_film_review(user_film_review)

    return await user_film_reviews_service.send_film_review(user_film_review)
