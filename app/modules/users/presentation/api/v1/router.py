from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.deps import get_principal
from app.modules.auth.shared.context import Principal

users_router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(security)]
)


@users_router.get("/me")
async def get_current_user(
    principal: Annotated[Principal, Depends(get_principal)],
) -> dict:
    return {
        "id": str(principal.id),
        "role": principal.role,
    }
