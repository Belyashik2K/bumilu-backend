from fastapi import APIRouter

from app.modules.auth.presentation.api.v1.router import auth_router
from app.modules.chat.presentation.api.v1 import chat_router
from app.modules.favourites.presentation.api.v1 import favourites_router
from app.modules.reviews.presentation.api.v1 import reviews_router
from app.modules.staff.presentation.api.v1 import staff_router
from app.modules.users.presentation.api.v1 import users_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
v1_router.include_router(staff_router)
v1_router.include_router(reviews_router)
v1_router.include_router(favourites_router)
v1_router.include_router(chat_router)
