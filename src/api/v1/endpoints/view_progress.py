from http import HTTPStatus

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.api.v1.models.responses import InternalServerError, NotFound
from src.api.v1.models.view_progress import SaveViewProgressInput, ViewProgress
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.user_activity_service import UserActivityService


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
    user_view_service: UserActivityService = Depends(
        Provide[Container.user_activity_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    await user_view_service.insert_or_update_view_progress(
        dict(
            user_id=user_id,
            film_id=film_id,
            viewed_frame=body.viewed_frame,
        )
    )

    return await user_view_service.save_view_progress(
        film_id=film_id, viewed_frame=body.viewed_frame, user_id=user_id
    )


@router.get(
    "/view_progress/{film_id}",
    response_model=ViewProgress,
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="Получение временной метки о просмотре фильма.",
    description="Получить временную метку о просмотре фильма, на которой остановился пользователь.",
)
@inject
async def get_view_progress(
    film_id: str,
    user_view_service: UserActivityService = Depends(
        Provide[Container.user_activity_service]
    ),
    user_data=Depends(get_decoded_data),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await user_view_service.get_last_view_progress(
        dict(user_id=user_id, film_id=film_id)
    )
