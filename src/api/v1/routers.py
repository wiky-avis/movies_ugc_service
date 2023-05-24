from fastapi import APIRouter

from src.api.v1.endpoints import bookmarks, view_progress


router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(bookmarks.router)
router.include_router(view_progress.router)
