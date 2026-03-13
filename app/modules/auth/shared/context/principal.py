from dataclasses import dataclass

from app.core.shared.domain.value_objects.id import (
    PrincipalIdVO,
    SessionIdVO,
)
from app.core.shared.enums import UserRoleEnum


@dataclass(frozen=True, slots=True)
class Principal:
    id: PrincipalIdVO
    session_id: SessionIdVO
    role: UserRoleEnum

    def is_admin(self) -> bool:
        return self.role == UserRoleEnum.ADMIN
