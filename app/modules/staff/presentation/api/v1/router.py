from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from app.core.presentation.api.schemas.pagination import OffsetPaginationDep
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.staff.deps import get_staff_principal
from app.modules.auth.shared.context import Principal
from app.modules.staff.application.commands.create_member.command import (
    CreateStaffMemberCommand,
)
from app.modules.staff.application.commands.create_member.handler import (
    CreateStaffMemberCommandHandler,
)
from app.modules.staff.application.queries.get.handler import GetStaffMemberQueryHandler
from app.modules.staff.application.queries.get.query import GetStaffMemberQuery
from app.modules.staff.application.queries.get_all.handler import (
    GetStaffMembersListQueryHandler,
)
from app.modules.staff.application.queries.get_all.query import GetStaffMembersListQuery
from app.modules.staff.presentation.api.schemas.common import (
    AuthenticatedStaffMemberInfoSchema,
    CreateStaffMemberRequestSchema,
    PaginatedFullStaffMemberInfoSchema,
)

staff_router = APIRouter(
    prefix="/staff",
    tags=["Staff"],
    dependencies=[Depends(security)],
)


@staff_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses=generate_responses_for_endpoint(),
)
@inject
async def create_staff_member(
    handler: FromDishka[CreateStaffMemberCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: CreateStaffMemberRequestSchema,
) -> None:
    await handler(
        CreateStaffMemberCommand(
            actor_id=principal.id.value,
            name=data.name,
            email=str(data.email),
            password=data.password,
            role=data.role,
        )
    )


@staff_router.get("", responses=generate_responses_for_endpoint())
@inject
async def get_all_staff_members(
    handler: FromDishka[GetStaffMembersListQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    pagination: OffsetPaginationDep,
) -> PaginatedFullStaffMemberInfoSchema:
    result = await handler(
        GetStaffMembersListQuery(
            actor_id=principal.id.value,
            limit=pagination.limit,
            offset=pagination.offset,
        )
    )
    return PaginatedFullStaffMemberInfoSchema.model_validate(
        result, from_attributes=True
    )


@staff_router.get("/me", responses=generate_responses_for_endpoint())
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
