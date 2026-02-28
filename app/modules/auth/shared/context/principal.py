from dataclasses import dataclass

from app.core.shared.domain.value_objects.id import (
    SessionIdVO,
    UserIdVO,
)
from app.core.shared.enums import UserRoleEnum


@dataclass(frozen=True, slots=True)
class Principal:
    id: UserIdVO
    session_id: SessionIdVO
    role: UserRoleEnum
