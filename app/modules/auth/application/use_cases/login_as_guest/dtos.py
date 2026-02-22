from dataclasses import (
    dataclass,
    field,
)

from app.core.shared.domain.value_objects.id import DeviceIdVO
from app.core.shared.enums import (
    DevicePlatformEnum,
)
from app.modules.auth.application.use_cases.shared_dtos import (
    IssuedTokensDTO,
)


@dataclass(slots=True, kw_only=True, frozen=True)
class LoginAsGuestInputDTO:
    device_id: DeviceIdVO
    device_platform: DevicePlatformEnum
    device_name: str | None = field(default=None)
    app_version: str


@dataclass(slots=True, kw_only=True, frozen=True)
class LoginAsGuestOutputDTO(IssuedTokensDTO): ...
