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
from app.modules.auth.presentation.api.v1.staff.deps import get_staff_principal
from app.modules.auth.shared.context import Principal
from app.modules.staff.application.queries.get.handler import GetStaffMemberQueryHandler
from app.modules.staff.application.queries.get.query import GetStaffMemberQuery
from app.modules.staff.presentation.api.schemas.common import (
    AuthenticatedStaffMemberInfoSchema,
)

staff_router = APIRouter(
    prefix="/staff",
    tags=["Staff"],
    dependencies=[Depends(security)],
)


@staff_router.get(
    "/me", responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED)
)
@inject
async def get_current_staff_member(
    handler: FromDishka[GetStaffMemberQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> AuthenticatedStaffMemberInfoSchema:
    result = await handler(
        GetStaffMemberQuery(
            staff_member_id=principal.id.value,
        )
    )
    return AuthenticatedStaffMemberInfoSchema.model_validate(
        result, from_attributes=True
    )
