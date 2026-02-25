from fastapi import (
    APIRouter,
    Depends,
)

from app.modules.auth.presentation.api import security

users_router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(security)]
)


@users_router.get("/me")
async def get_current_user() -> dict:
    return {"id": "user_id", "username": "current_user", "email": "test@bumilu.ru"}
