from fastapi import APIRouter

from .categories.admin_router import admin_place_categories_router
from .categories.user_router import user_place_categories_router
from .places.router import user_places_router

places_router = APIRouter()
places_router.include_router(user_place_categories_router)
places_router.include_router(admin_place_categories_router)
places_router.include_router(user_places_router)
