from http import HTTPStatus

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.api.v1.models.responses import InternalServerError
from src.api.v1.models.review_likes import (
    LikeEventType,
    ReviewLikeInput,
    ReviewLikeModel,
)
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.user_review_likes import UserReviewLikesService


router = APIRouter()


@router.post(
    "/review_likes/like",
    responses={500: {"model": InternalServerError}},
    summary="Добавить лайк к рецензии.",
    description="Добавить лайк к рецензии.",
)
@inject
async def add_like(
    body: ReviewLikeInput = Body(...),
    user_review_likes_service: UserReviewLikesService = Depends(
        Provide[Container.user_review_likes_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )
    user_like_data = ReviewLikeModel(
        review_id=body.review_id,
        event_type=LikeEventType.LIKE,
        user_id=user_id,  # type: ignore[arg-type]
    )

    await user_review_likes_service.add_like(user_like_data)

    return await user_review_likes_service.send_event_review_like(
        user_like_data
    )


@router.post(
    "/review_likes/dislike",
    responses={500: {"model": InternalServerError}},
    summary="Добавить дизлайк к рецензии.",
    description="Добавить дизлайк к рецензии.",
)
@inject
async def add_dislike(
    body: ReviewLikeInput = Body(...),
    user_review_likes_service: UserReviewLikesService = Depends(
        Provide[Container.user_review_likes_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )
    user_like_data = ReviewLikeModel(
        review_id=body.review_id,
        event_type=LikeEventType.DISLIKE,
        user_id=user_id,  # type: ignore[arg-type]
    )

    await user_review_likes_service.add_dislike(user_like_data)

    return await user_review_likes_service.send_event_review_like(
        user_like_data
    )
