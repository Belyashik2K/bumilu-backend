from fastapi import APIRouter

from app.core.presentation.api.v1.internal import internal_router

v1_router = APIRouter(
    prefix="/v1",
)
v1_router.include_router(internal_router)
