from fastapi import APIRouter

from app.modules.auth.presentation.api.v1 import auth_router
from app.modules.users.presentation.api.v1 import users_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
