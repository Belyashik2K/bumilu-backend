from dataclasses import (
    dataclass,
)
from uuid import UUID

from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class StaffMemberInfoView:
    id: UUID
    email: str
    role: StaffRoleEnum
