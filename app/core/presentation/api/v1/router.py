from fastapi import APIRouter

from app.core.presentation.api.v1 import internal_router
from app.modules.auth.presentation.api.v1 import auth_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(internal_router)
v1_router.include_router(auth_router)
