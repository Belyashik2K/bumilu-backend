from dataclasses import dataclass
from uuid import UUID

from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateStaffMemberCommand:
    actor_id: UUID
    name: str
    email: str
    password: str
    role: StaffRoleEnum
