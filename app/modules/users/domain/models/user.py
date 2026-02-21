from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Self

from app.core.shared.domain.value_objects.id import (
    UserIdVO,
)
from app.core.shared.enums import UserRoleEnum
from app.core.shared.utils import get_current_dt
from app.modules.users.domain.value_objects import EmailVO


@dataclass(slots=True, kw_only=True)
class User:
    id: UserIdVO
    email: EmailVO | None = field(default=None)
    email_verified_at: datetime | None = field(default=None)
    role: UserRoleEnum = field(default=UserRoleEnum.GUEST)

    @classmethod
    def create_guest(cls) -> Self:
        return cls(id=UserIdVO.new(), role=UserRoleEnum.GUEST)

    @classmethod
    def create_verified(
        cls, *, email: EmailVO, role: UserRoleEnum = UserRoleEnum.USER
    ) -> Self:
        if role is UserRoleEnum.GUEST:
            raise ValueError("Guest cannot be created as verified.")
        now = get_current_dt()
        return cls(
            id=UserIdVO.new(),
            email=email,
            email_verified_at=now,
            role=role,
        )

    def attach_email(self, email: EmailVO) -> None:
        if self.email is not None and self.email != email:
            raise ValueError("Email already set.")
        self.email = email
        self.email_verified_at = None

    def verify_email(self) -> None:
        if self.email is None:
            raise ValueError("Cannot verify email without email address.")
        if self.email_verified_at is not None:
            return
        self.email_verified_at = get_current_dt()
        if self.role is UserRoleEnum.GUEST:
            self.role = UserRoleEnum.USER
