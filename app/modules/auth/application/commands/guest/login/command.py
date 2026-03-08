from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.shared.enums import (
    DevicePlatformEnum,
)
from app.modules.auth.application.commands.shared_dtos import (
    IssuedTokensDTO,
)


@dataclass(slots=True, kw_only=True, frozen=True)
class LoginAsGuestCommand:
    device_id: UUID
    device_platform: DevicePlatformEnum
    device_name: str | None = field(default=None)
    app_version: str


@dataclass(slots=True, kw_only=True, frozen=True)
class LoginAsGuestCommandResult(IssuedTokensDTO): ...
