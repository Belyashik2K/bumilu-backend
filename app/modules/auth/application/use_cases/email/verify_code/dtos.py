from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.shared.enums import DevicePlatformEnum
from app.modules.auth.application.use_cases.shared_dtos import IssuedTokensDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class VerifyEmailCodeAtLoginInputDTO:
    email: str
    code: str
    device_id: UUID
    device_platform: DevicePlatformEnum
    device_name: str | None = field(default=None)
    app_version: str
    # TODO: Compose it in DeviceInfoVO


@dataclass(frozen=True, slots=True, kw_only=True)
class VerifyEmailCodeAtLoginOutputDTO(IssuedTokensDTO): ...
