from app.core.domain.value_objects.string.object import BaseStringVO
from app.modules.staff.domain.value_objects.staff_password.exception import (
    InvalidStaffMemberPassword,
)


class StaffMemberPasswordVO(BaseStringVO):
    min_length = 8
    max_length = 32

    @classmethod
    def additional_validate(cls, value: str) -> str:
        if not any(char.isupper() for char in value):
            raise InvalidStaffMemberPassword(
                "Password must contain at least one uppercase letter."
            )
        if not any(char.islower() for char in value):
            raise InvalidStaffMemberPassword(
                "Password must contain at least one lowercase letter."
            )
        if not any(char.isdigit() for char in value):
            raise InvalidStaffMemberPassword(
                "Password must contain at least one digit."
            )
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in value):
            raise InvalidStaffMemberPassword(
                "Password must contain at least one special character."
            )
        return value
