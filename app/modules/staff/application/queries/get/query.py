from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetStaffMemberQuery:
    staff_member_id: UUID
