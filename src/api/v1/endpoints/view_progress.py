from http import HTTPStatus

import dpath
import orjson
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_pagination import Page
from pydantic import BaseModel, Field

from src.api.v1.models.responses import InternalServerError, NotFound
from src.api.v1.models.view_progress import SaveViewProgressInput, ViewProgress
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.user_view_history import UserViewHistoryService


router = APIRouter()


@router.post(
    "/view_progress/{film_id}",
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="Сохранение временной метки о просмотре фильма.",
    description="Отправить сообщение с временной меткой о просмотре фильма в топик брокера сообщений.",
)
@inject
async def saving_view_progress(
    film_id: str,
    body: SaveViewProgressInput = Body(...),
    user_view_service: UserViewHistoryService = Depends(
        Provide[Container.user_view_history_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )
    user_view_progress_data = dict(
        film_id=film_id,
        viewed_frame=body.viewed_frame,
        user_id=user_id,
    )

    await user_view_service.insert_or_update_view_progress(
        user_view_progress_data
    )

    return await user_view_service.send_view_progress(user_view_progress_data)


@router.get(
    "/view_progress/{film_id}",
    response_model=ViewProgress,
    responses={404: {"model": NotFound}},
    summary="Получение временной метки о просмотре фильма.",
    description="Получить временную метку о просмотре фильма, на которой остановился пользователь.",
)
@inject
async def get_view_progress(
    film_id: str,
    user_view_service: UserViewHistoryService = Depends(
        Provide[Container.user_view_history_service]
    ),
    user_data=Depends(get_decoded_data),
) -> ViewProgress:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await user_view_service.get_last_view_progress(
        dict(user_id=user_id, film_id=film_id)
    )


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FilmOut(BaseModel):
    film_id: str = Field(alias="_id")
    count: int

    class Config:
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


Page = Page.with_custom_options(
    size=Field(20, ge=1, le=100),
)


@router.get(
    "/watching_now",
    summary="Список фильмов которые сейчас смотрят.",
    description="Список film_id которые пользователи сейчас смотрят, отсортированные по количеству пользователей.",
)
@inject
async def watching_now(
    user_view_service: UserViewHistoryService = Depends(
        Provide[Container.user_view_history_service]
    ),
) -> Page[FilmOut]:
    res = await user_view_service.get_films_ids_watching_now()
    return res
