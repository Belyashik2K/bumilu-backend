from dataclasses import (
    dataclass,
    field,
)

from app.core.shared.domain.value_objects.id import DeviceIdVO
from app.core.shared.enums import DevicePlatformEnum


@dataclass(slots=True, kw_only=True, frozen=True)
class LoginAsGuestInputDTO:
    device_id: DeviceIdVO
    platform: DevicePlatformEnum
    app_version: str
    name: str | None = field(default=None)


@dataclass(slots=True, kw_only=True, frozen=True)
class LoginAsGuestOutputDTO: ...
