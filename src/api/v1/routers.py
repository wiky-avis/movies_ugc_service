from fastapi import APIRouter

from src.api.v1.endpoints import bookmarks, film_scores, view_progress, film_reviews

router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(bookmarks.router)
router.include_router(view_progress.router)
router.include_router(film_scores.router)
router.include_router(film_reviews.router)
