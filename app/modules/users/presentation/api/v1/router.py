from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.users.deps import get_principal
from app.modules.auth.shared.context import Principal
from app.modules.users.application.queries.get import (
    GetUserQuery,
    GetUserQueryHandler,
)
from app.modules.users.presentation.api.schemas.common import (
    AuthenticatedUserInfoSchema,
)

users_router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(security)]
)


@users_router.get(
    "/me", responses=generate_responses_for_endpoint(status.HTTP_404_NOT_FOUND)
)
@inject
async def get_current_user(
    handler: FromDishka[GetUserQueryHandler],
    principal: Annotated[Principal, Depends(get_principal)],
) -> AuthenticatedUserInfoSchema:
    result = await handler(
        GetUserQuery(
            user_id=principal.id.value,
        )
    )
    return AuthenticatedUserInfoSchema.model_validate(result, from_attributes=True)
