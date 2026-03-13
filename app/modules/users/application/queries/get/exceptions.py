from app.core.shared.domain.value_objects.id import PrincipalIdVO
from app.core.shared.exceptions.application.base import ApplicationNotFoundException


class UserNotFound(ApplicationNotFoundException):  # TODO: Move to shared exceptions
    def __init__(self, user_id: PrincipalIdVO) -> None:
        super().__init__(
            message="User not found",
            details={"user_id": str(user_id)},
        )
