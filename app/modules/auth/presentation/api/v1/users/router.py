from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.application.commands.logout import (
    LogoutCommand,
    LogoutCommandHandler,
)
from app.modules.auth.application.commands.user.email import (
    RequestEmailCodeAtLoginCommand,
    RequestEmailCodeAtLoginCommandHandler,
    VerifyEmailCodeAtLoginCommand,
    VerifyEmailCodeAtLoginCommandHandler,
)
from app.modules.auth.application.commands.user.guest import (
    LoginAsGuestCommand,
    LoginAsGuestCommandHandler,
)
from app.modules.auth.application.commands.user.refresh_session import (
    RefreshAuthSessionCommand,
    RefreshAuthSessionCommandHandler,
)
from app.modules.auth.presentation.api.schemas.common import (
    RefreshAuthSessionRequestSchema,
)
from app.modules.auth.presentation.api.schemas.logout import LogoutRequestSchema
from app.modules.auth.presentation.api.schemas.user.device import (
    DeviceInfoHeadersSchema,
    get_device_info_headers,
)
from app.modules.auth.presentation.api.schemas.user.login import (
    RequestEmailCodeAtLoginRequestSchema,
    SuccessfulUserLoginSchema,
    VerifyEmailCodeAtLoginRequestSchema,
)
from app.modules.auth.presentation.api.schemas.user.refresh import (
    RefreshUserAuthSessionResponseSchema,
)

users_auth_router = APIRouter(
    tags=["User Authentication"],
    prefix="/users",
)


@users_auth_router.post("/guest", responses=generate_responses_for_endpoint())
@inject
async def login_as_guest(
    handler: FromDishka[LoginAsGuestCommandHandler],
    headers: Annotated[DeviceInfoHeadersSchema, Depends(get_device_info_headers)],
) -> SuccessfulUserLoginSchema:
    result = await handler(
        LoginAsGuestCommand(
            device_id=headers.device_id,
            device_platform=headers.device_platform,
            device_name=headers.device_name,
            app_version=headers.app_version,
        )
    )
    return SuccessfulUserLoginSchema.model_validate(result, from_attributes=True)


@users_auth_router.post(
    "/email/request-code",
    responses=generate_responses_for_endpoint(),
)
@inject
async def request_email_code(
    handler: FromDishka[RequestEmailCodeAtLoginCommandHandler],
    data: RequestEmailCodeAtLoginRequestSchema,
    headers: Annotated[DeviceInfoHeadersSchema, Depends(get_device_info_headers)],
) -> dict:
    await handler(RequestEmailCodeAtLoginCommand(email=str(data.email)))
    return {}


@users_auth_router.post(
    "/email/verify-code",
    responses=generate_responses_for_endpoint(),
)
@inject
async def verify_email_login(
    handler: FromDishka[VerifyEmailCodeAtLoginCommandHandler],
    data: VerifyEmailCodeAtLoginRequestSchema,
    headers: Annotated[DeviceInfoHeadersSchema, Depends(get_device_info_headers)],
) -> SuccessfulUserLoginSchema:
    result = await handler(
        VerifyEmailCodeAtLoginCommand(
            email=str(data.email),
            code=data.code,
            device_id=headers.device_id,
            device_platform=headers.device_platform,
            device_name=headers.device_name,
            app_version=headers.app_version,
        )
    )
    return SuccessfulUserLoginSchema.model_validate(result, from_attributes=True)


@users_auth_router.post(
    "/refresh",
    responses=generate_responses_for_endpoint(),
)
@inject
async def refresh(
    handler: FromDishka[RefreshAuthSessionCommandHandler],
    data: RefreshAuthSessionRequestSchema,
    headers: Annotated[DeviceInfoHeadersSchema, Depends(get_device_info_headers)],
) -> RefreshUserAuthSessionResponseSchema:
    result = await handler(
        RefreshAuthSessionCommand(
            refresh_token=data.refresh_token,
            device_id=headers.device_id,
        )
    )
    return RefreshUserAuthSessionResponseSchema.model_validate(
        result, from_attributes=True
    )


@users_auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(),
)
@inject
async def logout(
    handler: FromDishka[LogoutCommandHandler],
    data: LogoutRequestSchema,
    headers: Annotated[DeviceInfoHeadersSchema, Depends(get_device_info_headers)],
) -> None:
    await handler(
        LogoutCommand(
            refresh_token=data.refresh_token,
            device_id=headers.device_id,
        )
    )
