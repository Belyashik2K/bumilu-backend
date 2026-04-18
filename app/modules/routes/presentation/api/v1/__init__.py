from fastapi import APIRouter

from .admin_router import admin_routes_router
from .user_router import user_routes_router

routes_router = APIRouter()
routes_router.include_router(user_routes_router)
routes_router.include_router(admin_routes_router)
