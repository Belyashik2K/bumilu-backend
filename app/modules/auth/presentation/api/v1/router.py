from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from app.core.shared.domain.value_objects.id import DeviceIdVO
from app.modules.auth.application.use_cases.login_as_guest import (
    LoginAsGuestInputDTO,
    LoginAsGuestUseCase,
)
from app.modules.auth.presentation.api.schemas.login import (
    LoginAsGuestRequestSchema,
    LoginAsGuestResponseSchema,
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("/login/guest")
@inject
async def login_as_guest(
    uc: FromDishka[LoginAsGuestUseCase],
    data: LoginAsGuestRequestSchema,
) -> LoginAsGuestResponseSchema:
    result = await uc(
        LoginAsGuestInputDTO(
            device_id=DeviceIdVO.from_uuid(data.device_id),
            device_platform=data.device_platform,
            device_name=data.device_name,
            app_version=data.app_version,
        )
    )
    return LoginAsGuestResponseSchema.model_validate(result, from_attributes=True)


@auth_router.post("/login/email/request")
async def request_email_code() -> None:
    raise NotImplementedError


@auth_router.post("/login/email/verify")
async def verify_email_login() -> None:
    raise NotImplementedError


@auth_router.post("/refresh")
async def refresh() -> None:
    raise NotImplementedError


@auth_router.post("/logout")
async def logout() -> None:
    raise NotImplementedError
