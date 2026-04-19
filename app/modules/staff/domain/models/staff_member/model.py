from dataclasses import dataclass
from typing import Self

from app.core.domain.value_objects.id import (
    PrincipalIdVO,
)
from app.modules.staff.domain.value_objects.staff_email.object import StaffMemberEmailVO
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


@dataclass(slots=True, kw_only=True)
class StaffMember:
    id: PrincipalIdVO
    name: str
    email: StaffMemberEmailVO
    password_hash: str
    role: StaffRoleEnum

    @classmethod
    def create(
        cls,
        *,
        id: PrincipalIdVO,
        name: str,
        email: StaffMemberEmailVO,
        password_hash: str,
        role: StaffRoleEnum,
    ) -> Self:
        return cls(
            id=id,
            name=name,
            email=email,
            password_hash=password_hash,
            role=role,
        )
