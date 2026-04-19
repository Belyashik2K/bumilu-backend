from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status
from starlette.responses import Response

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.application.commands.logout import (
    LogoutCommand,
    LogoutCommandHandler,
)
from app.modules.auth.application.commands.staff.login import (
    LoginAsStaffMemberCommand,
    LoginAsStaffMemberCommandHandler,
)
from app.modules.auth.application.commands.staff.refresh_session import (
    RefreshStaffMemberAuthSessionCommand,
    RefreshStaffMemberAuthSessionCommandHandler,
    RefreshStaffMemberAuthSessionCommandResult,
)
from app.modules.auth.presentation.api.schemas.staff.common import (
    SuccessfulStaffMemberLoginSchema,
)
from app.modules.auth.presentation.api.schemas.staff.login import (
    StaffMemberLoginRequestSchema,
)
from app.modules.auth.presentation.api.schemas.staff.refresh import (
    RefreshStaffMemberAuthSessionResponseSchema,
)
from app.modules.auth.presentation.api.v1.staff.deps import (
    require_cookie_refresh_token,
)

staff_auth_router = APIRouter(tags=["Staff Auth"], prefix="/staff")


@staff_auth_router.post(
    "/login",
    responses=generate_responses_for_endpoint(),
)
@inject
async def staff_login(
    response: Response,
    data: StaffMemberLoginRequestSchema,
    handler: FromDishka[LoginAsStaffMemberCommandHandler],
) -> SuccessfulStaffMemberLoginSchema:
    result = await handler(
        LoginAsStaffMemberCommand(
            email=str(data.email),
            password=data.password,
        )
    )
    response.set_cookie(
        key="bumilu",  # TODO: make cookie name configurable
        value=result.refresh.token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=result.refresh.expires_in,
    )
    return SuccessfulStaffMemberLoginSchema.model_validate(result, from_attributes=True)


@staff_auth_router.post(
    "/refresh",
    responses=generate_responses_for_endpoint(),
)
@inject
async def staff_refresh(
    response: Response,
    handler: FromDishka[RefreshStaffMemberAuthSessionCommandHandler],
    refresh_token: str = Depends(require_cookie_refresh_token),
) -> RefreshStaffMemberAuthSessionResponseSchema:
    result: RefreshStaffMemberAuthSessionCommandResult = await handler(
        RefreshStaffMemberAuthSessionCommand(
            refresh_token=refresh_token,
        )
    )
    response.set_cookie(
        key="bumilu",  # TODO: make cookie name configurable
        value=result.refresh.token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=result.refresh.expires_in,
    )
    return RefreshStaffMemberAuthSessionResponseSchema.model_validate(
        result, from_attributes=True
    )


@staff_auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(),
)
@inject
async def staff_logout(
    response: Response,
    handler: FromDishka[LogoutCommandHandler],
    refresh_token: str = Depends(require_cookie_refresh_token),
) -> None:
    await handler(LogoutCommand(refresh_token=refresh_token))
    response.delete_cookie(key="bumilu")  # TODO: make cookie name configurable
