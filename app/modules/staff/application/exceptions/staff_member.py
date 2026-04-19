from app.core.domain.value_objects.id import PrincipalIdVO
from app.core.exceptions.application.base import (
    ApplicationConflictException,
    ApplicationForbiddenException,
    ApplicationNotFoundException,
)
from app.modules.staff.domain.value_objects.staff_email import StaffMemberEmailVO
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


class StaffMemberNotFound(ApplicationNotFoundException):
    def __init__(self, staff_member_id: PrincipalIdVO) -> None:
        super().__init__(
            message="Staff member not found.",
            details={"staff_member_id": str(staff_member_id)},
        )


class StaffMemberWithGivenEmailAlreadyExists(ApplicationConflictException):
    def __init__(self, email: StaffMemberEmailVO) -> None:
        super().__init__(
            message=f"Staff member with email {email} already exists.",
            details={"email": email},  # TODO: kwargs for details in base exception
        )


class ActorRoleNotAllowedToPerformAction(ApplicationForbiddenException):
    def __init__(self, actor_role: StaffRoleEnum | None, action: str) -> None:
        super().__init__(
            message=f"Actor with role {actor_role or "UNKNOWN"} is not allowed to perform action '{action}'.",
            details={"actor_role": actor_role, "action": action},
        )


class MultipleOwnersNotAllowed(ApplicationConflictException):
    def __init__(self) -> None:
        super().__init__(
            message="Multiple staff members with role OWNER are not allowed.",
        )
