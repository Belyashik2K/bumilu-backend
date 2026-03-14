from app.core.shared.domain.value_objects.id import PrincipalIdVO
from app.core.shared.exceptions.application.base import ApplicationNotFoundException


class StaffMemberNotFound(
    ApplicationNotFoundException
):  # TODO: Move to shared exceptions
    def __init__(self, staff_member_id: PrincipalIdVO) -> None:
        super().__init__(
            message="Staff member not found.",
            details={"staff_member_id": str(staff_member_id)},
        )
