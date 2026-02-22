from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from app.modules.auth.application.use_cases.email.request_code import (
    RequestEmailCodeAtLoginUseCase,
)
from app.modules.auth.application.use_cases.email.verify_code import (
    VerifyEmailCodeAtLoginUseCase,
)
from app.modules.auth.application.use_cases.guest.login import (
    LoginAsGuestInputDTO,
    LoginAsGuestUseCase,
)
from app.modules.auth.application.use_cases.logout import LogoutInputDTO
from app.modules.auth.application.use_cases.logout.use_case import LogoutUseCase
from app.modules.auth.application.use_cases.refresh_session import (
    RefreshAuthSessionInputDTO,
)
from app.modules.auth.application.use_cases.refresh_session.use_case import (
    RefreshAuthSessionUseCase,
)
from app.modules.auth.presentation.api.schemas.login import (
    LoginAsGuestRequestSchema,
    LoginAsGuestResponseSchema,
)
from app.modules.auth.presentation.api.schemas.logout import LogoutRequestSchema
from app.modules.auth.presentation.api.schemas.refresh import (
    RefreshAuthSessionRequestSchema,
    RefreshAuthSessionResponseSchema,
)

auth_router = APIRouter(
    prefix="/auth/sessions",
    tags=["Auth"],
)


@auth_router.post("/guest")
@inject
async def login_as_guest(
    uc: FromDishka[LoginAsGuestUseCase],
    data: LoginAsGuestRequestSchema,
) -> LoginAsGuestResponseSchema:
    result = await uc(
        LoginAsGuestInputDTO(
            device_id=data.device_id,
            device_platform=data.device_platform,
            device_name=data.device_name,
            app_version=data.app_version,
        )
    )
    return LoginAsGuestResponseSchema.model_validate(result, from_attributes=True)


@auth_router.post("/email/request")
async def request_email_code(
    uc: FromDishka[RequestEmailCodeAtLoginUseCase],
) -> None:
    raise NotImplementedError


@auth_router.post("/email/verify")
@inject
async def verify_email_login(
    uc: FromDishka[VerifyEmailCodeAtLoginUseCase],
) -> None:
    raise NotImplementedError


@auth_router.post("/refresh")
@inject
async def refresh(
    uc: FromDishka[RefreshAuthSessionUseCase], data: RefreshAuthSessionRequestSchema
) -> RefreshAuthSessionResponseSchema:
    result = await uc(
        RefreshAuthSessionInputDTO(
            refresh_token=data.refresh_token,
            device_id=data.device_id,
        )
    )
    return RefreshAuthSessionResponseSchema.model_validate(result, from_attributes=True)


@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def logout(uc: FromDishka[LogoutUseCase], data: LogoutRequestSchema) -> None:
    await uc(
        LogoutInputDTO(
            refresh_token=data.refresh_token,
            device_id=data.device_id,
        )
    )
