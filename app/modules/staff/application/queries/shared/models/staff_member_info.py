from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class StaffMemberInfoReadModel:
    id: UUID
    email: str
    role: StaffRoleEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class StaffMemberFullInfoReadModel(StaffMemberInfoReadModel):
    name: str
    created_at: datetime
