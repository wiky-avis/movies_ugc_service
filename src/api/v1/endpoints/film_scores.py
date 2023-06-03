from http import HTTPStatus
from typing import Annotated

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate

from src.api.v1.models.film_scores import (
    DeleteFilmScoreInput,
    FilmAvgScore,
    ScoreEventType,
    SetFilmScoreInput,
    UserFilmScore,
)
from src.api.v1.models.responses import (
    InternalServerError,
    NotAuthorized,
    NotFound,
)
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.film_scores import UserFilmScoresService


router = APIRouter()


@router.post(
    "/film_scores",
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
    body: SetFilmScoreInput = Body(...),
    user_film_scores_service: UserFilmScoresService = Depends(
        Provide[Container.user_film_scores_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    score_data = UserFilmScore(
        film_id=body.film_id,
        user_id=user_id,  # type: ignore[arg-type]
        score=body.score,
    )

    await user_film_scores_service.set_score(score_data)

    return await user_film_scores_service.send_event(
        score_data, ScoreEventType.SET
    )


@router.delete(
    "/film_scores",
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
    body: DeleteFilmScoreInput = Body(...),
    user_film_scores_service: UserFilmScoresService = Depends(
        Provide[Container.user_film_scores_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    score_data = UserFilmScore(
        film_id=body.film_id,
        user_id=user_id,  # type: ignore[arg-type]
        score=0,
    )

    await user_film_scores_service.delete_score(score_data)

    await user_film_scores_service.send_event(
        score_data, ScoreEventType.DELETE
    )

    return JSONResponse("Score successfully deleted", HTTPStatus.NO_CONTENT)


@router.get(
    "/film_scores/top",
    responses={
        404: {"model": NotFound},
        500: {"model": InternalServerError},
        401: {"model": NotAuthorized},
    },
    summary="Получение топа фильмов по пользовательской оценке",
    description="Возвращает список фильмов со средней оценкой и кол-вом отзывов",
)
@inject
async def get_top_films_by_score(
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    user_film_scores_service: UserFilmScoresService = Depends(
        Provide[Container.user_film_scores_service]
    ),
) -> Page[FilmAvgScore]:
    result = await user_film_scores_service.get_top_scores(limit=limit)
    return paginate(sequence=result)


@router.get(
    "/film_scores",
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
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await user_film_scores_service.get_user_score(
        film_id=film_id, user_id=str(user_id)
    )
