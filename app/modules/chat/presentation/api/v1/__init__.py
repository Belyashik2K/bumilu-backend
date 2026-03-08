from fastapi import APIRouter

from .admin_router import admin_chat_router
from .user_router import user_chat_router

chat_router = APIRouter()
chat_router.include_router(user_chat_router)
chat_router.include_router(admin_chat_router)
