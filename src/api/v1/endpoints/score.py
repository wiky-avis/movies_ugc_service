from http import HTTPStatus

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.api.v1.models.responses import InternalServerError, NotFound, NotAuthorized
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.film_scores import UserFilmScoresService


router = APIRouter()


@router.post(
    "/score-film/{film_id}",
    responses={
        404: {"model": NotFound},
        500: {"model": InternalServerError},
        401: {"model": NotAuthorized},
    },
    summary="",
    description="",
)
@inject
async def set_film_score(
    film_id: str,
    user_film_scores_service: UserFilmScoresService = Depends(
        Provide[Container.user_film_scores_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    score = dpath.get(user_data, "score", default=None)
    if not user_id or not score:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    score_data = dict(
        film_id=film_id,
        user_id=user_id,
        score=score,
    )

    await user_film_scores_service.set_score(score_data)

    return await user_film_scores_service.send_event(score_data, "set")


@router.delete(
    "/score-film/{film_id}",
    responses={
        404: {"model": NotFound},
        500: {"model": InternalServerError},
        401: {"model": NotAuthorized},
    },
    summary="",
    description="",
)
@inject
async def delete_film_score(
    film_id: str,
    user_film_scores_service: UserFilmScoresService = Depends(
        Provide[Container.user_film_scores_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    score = dpath.get(user_data, "score", default=None)
    if not user_id or not score:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    score_data = dict(
        film_id=film_id,
        user_id=user_id,
        score=score,
    )

    await user_film_scores_service.delete_score(score_data)

    return await user_film_scores_service.send_event(score_data, "delete")


@router.get(
    "/score-film/{film_id}",
    responses={
        404: {"model": NotFound},
        500: {"model": InternalServerError},
        401: {"model": NotAuthorized},
    },
    summary="",
    description="",
)
@inject
async def get_film_score(
    film_id: str,
    user_film_scores_service: UserFilmScoresService = Depends(
        Provide[Container.user_film_scores_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    score = dpath.get(user_data, "score", default=None)
    if not user_id or not score:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    score_data = dict(
        film_id=film_id,
        user_id=user_id,
        score=score,
    )

    return await user_film_scores_service.get_score(score_data)
