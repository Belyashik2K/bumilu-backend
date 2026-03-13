from fastapi import APIRouter

from app.modules.auth.presentation.api.v1.staff import staff_auth_router
from app.modules.auth.presentation.api.v1.users import users_auth_router

auth_router = APIRouter(
    prefix="/auth",
)
auth_router.include_router(users_auth_router)
auth_router.include_router(staff_auth_router)
