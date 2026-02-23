from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.application.use_cases.email.request_code import (
    RequestEmailCodeAtLoginInputDTO,
    RequestEmailCodeAtLoginUseCase,
)
from app.modules.auth.application.use_cases.email.verify_code import (
    VerifyEmailCodeAtLoginInputDTO,
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
    tags=["Auth"],
)


@auth_router.post("/guest", responses=generate_responses_for_endpoint())
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


@auth_router.post(
    "/email/request",
    responses=generate_responses_for_endpoint(
        status.HTTP_400_BAD_REQUEST,
    ),
)
@inject
async def request_email_code(
    uc: FromDishka[RequestEmailCodeAtLoginUseCase],
    data: RequestEmailCodeAtLoginRequestSchema,
) -> None:
    await uc(RequestEmailCodeAtLoginInputDTO(email=str(data.email)))


@auth_router.post(
    "/email/verify",
    responses=generate_responses_for_endpoint(
        status.HTTP_400_BAD_REQUEST,
    ),
)
@inject
async def verify_email_login(
    uc: FromDishka[VerifyEmailCodeAtLoginUseCase],
    data: VerifyEmailCodeAtLoginRequestSchema,
) -> VerifyEmailCodeAtLoginResponseSchema:
    result = await uc(
        VerifyEmailCodeAtLoginInputDTO(
            email=str(data.email),
            code=data.code,
            device_id=data.device_id,
            device_platform=data.device_platform,
            device_name=data.device_name,
            app_version=data.app_version,
        )
    )
    return VerifyEmailCodeAtLoginResponseSchema.model_validate(
        result, from_attributes=True
    )


@auth_router.post(
    "/refresh",
    responses=generate_responses_for_endpoint(
        status.HTTP_401_UNAUTHORIZED,
    ),
)
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
    responses=generate_responses_for_endpoint(),
)
@inject
async def logout(uc: FromDishka[LogoutUseCase], data: LogoutRequestSchema) -> None:
    await uc(
        LogoutInputDTO(
            refresh_token=data.refresh_token,
            device_id=data.device_id,
        )
    )
