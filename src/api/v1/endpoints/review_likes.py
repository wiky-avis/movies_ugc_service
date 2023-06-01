from http import HTTPStatus

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.api.v1.models.responses import InternalServerError
from src.api.v1.models.review_likes import EventType
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.user_review_likes import UserReviewLikesService


router = APIRouter()


@router.post(
    "/review_likes/{review_id}/like",
    responses={500: {"model": InternalServerError}},
    summary="",
    description="",
)
@inject
async def add_like(
    review_id: str,
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

    user_like_data = dict(
        review_id=review_id,
        event_type=EventType.LIKE,
        user_id=user_id,
    )

    await user_review_likes_service.add_like(user_like_data)

    return await user_review_likes_service.send_event_review_like(
        user_like_data
    )


@router.post(
    "/review_likes/{review_id}/dislike",
    responses={500: {"model": InternalServerError}},
    summary="",
    description="",
)
@inject
async def add_dislike(
    review_id: str,
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
    user_like_data = dict(
        review_id=review_id,
        event_type=EventType.DISLIKE,
        user_id=user_id,
    )

    await user_review_likes_service.add_dislike(user_like_data)

    return await user_review_likes_service.send_event_review_like(
        user_like_data
    )
