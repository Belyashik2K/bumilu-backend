from dataclasses import (
    dataclass,
    field,
)

from app.core.shared.enums import UserRoleEnum


@dataclass(slots=True, kw_only=True, frozen=True)
class UserInfoDTO:
    id: str
    email: str | None = field(default=None)
    role: UserRoleEnum
