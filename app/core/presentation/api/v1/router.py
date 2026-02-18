from fastapi import APIRouter

from app.core.presentation.api.v1.internal import router as internal_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(internal_router)
