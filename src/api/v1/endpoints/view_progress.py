from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from src.api.v1.models.view_progress import SaveViewProgressInput
from src.containers import Container
from src.services.user_activity_service import UserActivityService


router = APIRouter()


@router.post(
    "/view_progress/{film_id}",
)
@inject
async def saving_view_progress(
    film_id: str,
    body: SaveViewProgressInput = Body(...),
    user_view_service: UserActivityService = Depends(
        Provide[Container.user_activity_service]
    ),
) -> JSONResponse:
    return await user_view_service.save_view_progress(
        film_id=film_id, payload=body
    )
