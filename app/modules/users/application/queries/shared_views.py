from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.enums import UserRoleEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class UserInfoView:
    id: UUID
    email: str | None = field(default=None)
    role: UserRoleEnum
