from http import HTTPStatus

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.api.v1.models.bookmarks import (
    BookmarkEventType,
    UserBookmarkInput,
    UserBookmarkModel,
)
from src.api.v1.models.responses import InternalServerError
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.user_bookmarks import UserBookmarksService


router = APIRouter()


@router.post(
    "/bookmarks",
    responses={500: {"model": InternalServerError}},
    summary="Добавить фильм в закладки.",
    description="Добавление фильма в закладки пользователя.",
)
@inject
async def add_bookmark(
    body: UserBookmarkInput = Body(...),
    user_bookmarks_service: UserBookmarksService = Depends(
        Provide[Container.user_bookmarks_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    user_bookmark_data = UserBookmarkModel(
        film_id=body.film_id,
        event_type=BookmarkEventType.ADDED,
        user_id=user_id,  # type: ignore[arg-type]
    )

    await user_bookmarks_service.create_bookmark(user_bookmark_data)

    return await user_bookmarks_service.send_event_bookmark(user_bookmark_data)


@router.delete(
    "/bookmarks",
    responses={500: {"model": InternalServerError}},
    summary="Удалить фильм из закладок.",
    description="Удаление фильма из закладок поьзователя.",
)
@inject
async def delete_bookmark(
    film_id: str,
    user_bookmarks_service: UserBookmarksService = Depends(
        Provide[Container.user_bookmarks_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )
    user_bookmark_data = UserBookmarkModel(
        film_id=film_id,
        event_type=BookmarkEventType.DELETED,
        user_id=user_id,  # type: ignore[arg-type]
    )

    await user_bookmarks_service.delete_bookmark(user_bookmark_data)

    return await user_bookmarks_service.send_event_bookmark(user_bookmark_data)


@router.get(
    "/bookmarks",
    responses={500: {"model": InternalServerError}},
    summary="Список закладок пользователя.",
    description="Получить список film_id пользователя которые находятся у него в закладках.",
)
@inject
async def get_user_bookmarks(
    user_bookmarks_service: UserBookmarksService = Depends(
        Provide[Container.user_bookmarks_service]
    ),
    user_data=Depends(get_decoded_data),
) -> list[str]:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await user_bookmarks_service.get_bookmarks_by_user_id(
        user_id=user_id  # type: ignore[arg-type]
    )
