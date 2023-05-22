from http import HTTPStatus

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.api.v1.models.bookmarks import EventType
from src.api.v1.models.responses import InternalServerError, NotFound
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.user_bookmarks import UserBookmarksService


router = APIRouter()


@router.post(
    "/bookmarks/{film_id}",
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="",
    description="",
)
@inject
async def add_bookmark(
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

    user_bookmark_data = dict(
        film_id=film_id,
        event_type=EventType.ADDED,
        user_id=user_id,
    )

    await user_bookmarks_service.insert_or_update_bookmark(user_bookmark_data)

    return await user_bookmarks_service.send_event_bookmark(user_bookmark_data)


@router.delete(
    "/bookmarks/{film_id}",
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="",
    description="",
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
    user_bookmark_data = dict(
        film_id=film_id,
        event_type=EventType.DELETED,
        user_id=user_id,
    )

    await user_bookmarks_service.insert_or_update_bookmark(
        user_bookmark_data, is_deleted=True
    )

    return await user_bookmarks_service.send_event_bookmark(user_bookmark_data)


@router.get(
    "/bookmarks/list",
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="",
    description="",
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
        user_id=user_id
    )
