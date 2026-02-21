from dataclasses import (
    dataclass,
    field,
)

from app.core.shared.domain.value_objects.id import DeviceIdVO
from app.core.shared.enums import (
    DevicePlatformEnum,
    UserRoleEnum,
)


@dataclass(slots=True, kw_only=True, frozen=True)
class LoginAsGuestInputDTO:
    device_id: DeviceIdVO
    device_platform: DevicePlatformEnum
    device_name: str | None = field(default=None)
    app_version: str


@dataclass(slots=True, kw_only=True, frozen=True)
class TokenInfoDTO:
    token: str
    expires_in: int


@dataclass(slots=True, kw_only=True, frozen=True)
class UserInfoDTO:
    id: str
    role: UserRoleEnum


@dataclass(slots=True, kw_only=True, frozen=True)
class LoginAsGuestOutputDTO:
    access: TokenInfoDTO
    refresh: TokenInfoDTO
    user: UserInfoDTO
