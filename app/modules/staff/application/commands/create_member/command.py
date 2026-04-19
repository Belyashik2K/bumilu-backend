from dataclasses import dataclass

from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateStaffMemberCommand:
    name: str
    email: str
    password: str
    role: StaffRoleEnum
