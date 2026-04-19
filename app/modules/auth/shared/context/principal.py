from dataclasses import dataclass

from app.core.domain.value_objects.id import (
    PrincipalIdVO,
    SessionIdVO,
)
from app.core.enums import UserRoleEnum
from app.modules.auth.shared.enums import PrincipalTypeEnum
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


@dataclass(frozen=True, slots=True)
class Principal:
    id: PrincipalIdVO
    type: PrincipalTypeEnum
    role: UserRoleEnum | StaffRoleEnum
    session_id: SessionIdVO

    def is_staff(self) -> bool:
        return self.type == PrincipalTypeEnum.STAFF

    def is_user(self) -> bool:
        return self.type == PrincipalTypeEnum.USER
