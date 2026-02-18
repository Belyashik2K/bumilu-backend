from fastapi import APIRouter

from app.core.presentation.api.health import health_router
from app.core.presentation.api.v1 import v1_router

api_router = APIRouter()
api_router.include_router(v1_router)
api_router.include_router(health_router)
