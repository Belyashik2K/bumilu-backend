from dataclasses import (
    dataclass,
    field,
)

from app.core.enums import UserRoleEnum
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


@dataclass(slots=True, kw_only=True, frozen=True)
class AccountInfoDTO:  # TODO: remove this class
    id: str
    email: str | None = field(default=None)
    role: UserRoleEnum | StaffRoleEnum
