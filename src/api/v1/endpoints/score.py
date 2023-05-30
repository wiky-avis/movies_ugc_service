from http import HTTPStatus

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.api.v1.models.responses import (
    InternalServerError,
    NotAuthorized,
    NotFound,
)
from src.api.v1.models.scores import ScoreEventType
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
    summary="Поставить числовую оценку фильму",
    description="От пользователя приходит оценка от 1 до 10",
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

    return await user_film_scores_service.send_event(
        score_data, ScoreEventType.SET
    )


@router.delete(
    "/score-film/{film_id}",
    responses={
        404: {"model": NotFound},
        500: {"model": InternalServerError},
        401: {"model": NotAuthorized},
    },
    summary="Удалить поставленную оценку фильму",
    description="Пользователь передает фильм, с которого нужно снять оценку",
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

    return await user_film_scores_service.send_event(
        score_data, ScoreEventType.DELETE
    )


@router.get(
    "/score-film/{film_id}",
    responses={
        404: {"model": NotFound},
        500: {"model": InternalServerError},
        401: {"model": NotAuthorized},
    },
    summary="Получение оценки фильма, которую поставил пользователь",
    description="Передается числовая оценка по полученному фильму от 1 до 10",
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
