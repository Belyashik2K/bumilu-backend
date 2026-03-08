from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.application.commands.email import (
    RequestEmailCodeAtLoginCommand,
    RequestEmailCodeAtLoginCommandHandler,
    VerifyEmailCodeAtLoginCommand,
    VerifyEmailCodeAtLoginCommandHandler,
)
from app.modules.auth.application.commands.guest import (
    LoginAsGuestCommand,
    LoginAsGuestCommandHandler,
)
from app.modules.auth.application.commands.logout import LogoutInputDTO
from app.modules.auth.application.commands.logout.use_case import LogoutUseCase
from app.modules.auth.application.commands.refresh_session import (
    RefreshAuthSessionInputDTO,
)
from app.modules.auth.application.commands.refresh_session.use_case import (
    RefreshAuthSessionUseCase,
)
from app.modules.auth.presentation.api.schemas.device import (
    DeviceInfoHeadersSchema,
    get_device_info_headers,
)
from app.modules.auth.presentation.api.schemas.login import (
    LoginAsGuestResponseSchema,
    RequestEmailCodeAtLoginRequestSchema,
    VerifyEmailCodeAtLoginRequestSchema,
    VerifyEmailCodeAtLoginResponseSchema,
)
from app.modules.auth.presentation.api.schemas.logout import LogoutRequestSchema
from app.modules.auth.presentation.api.schemas.refresh import (
    RefreshAuthSessionRequestSchema,
    RefreshAuthSessionResponseSchema,
)

auth_router = APIRouter(
    prefix="/auth/sessions",
    tags=["Auth (mobile)"],
)


@auth_router.post("/guest", responses=generate_responses_for_endpoint())
@inject
async def login_as_guest(
    handler: FromDishka[LoginAsGuestCommandHandler],
    headers: Annotated[DeviceInfoHeadersSchema, Depends(get_device_info_headers)],
) -> LoginAsGuestResponseSchema:
    result = await handler(
        LoginAsGuestCommand(
            device_id=headers.device_id,
            device_platform=headers.device_platform,
            device_name=headers.device_name,
            app_version=headers.app_version,
        )
    )
    return LoginAsGuestResponseSchema.model_validate(result, from_attributes=True)


@auth_router.post(
    "/email/request",
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


@auth_router.post(
    "/email/verify",
    responses=generate_responses_for_endpoint(),
)
@inject
async def verify_email_login(
    handler: FromDishka[VerifyEmailCodeAtLoginCommandHandler],
    data: VerifyEmailCodeAtLoginRequestSchema,
    headers: Annotated[DeviceInfoHeadersSchema, Depends(get_device_info_headers)],
) -> VerifyEmailCodeAtLoginResponseSchema:
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
    return VerifyEmailCodeAtLoginResponseSchema.model_validate(
        result, from_attributes=True
    )


@auth_router.post(
    "/refresh",
    responses=generate_responses_for_endpoint(),
)
@inject
async def refresh(
    uc: FromDishka[RefreshAuthSessionUseCase],
    data: RefreshAuthSessionRequestSchema,
    headers: Annotated[DeviceInfoHeadersSchema, Depends(get_device_info_headers)],
) -> RefreshAuthSessionResponseSchema:
    result = await uc(
        RefreshAuthSessionInputDTO(
            refresh_token=data.refresh_token,
            device_id=headers.device_id,
        )
    )
    return RefreshAuthSessionResponseSchema.model_validate(result, from_attributes=True)


@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(),
)
@inject
async def logout(
    uc: FromDishka[LogoutUseCase],
    data: LogoutRequestSchema,
    headers: Annotated[DeviceInfoHeadersSchema, Depends(get_device_info_headers)],
) -> None:
    await uc(
        LogoutInputDTO(
            refresh_token=data.refresh_token,
            device_id=headers.device_id,
        )
    )
