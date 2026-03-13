from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Self

from app.core.shared.domain.value_objects.id import (
    PrincipalIdVO,
)
from app.core.shared.enums import UserRoleEnum
from app.core.shared.utils import get_current_dt
from app.modules.users.domain.models.user.exceptions import (
    CannotVerifyEmailWithoutEmail,
    UserEmailAlreadySet,
    VerifiedUserCannotBeGuest,
)
from app.modules.users.domain.value_objects import UserEmailVO


@dataclass(slots=True, kw_only=True)
class User:
    id: PrincipalIdVO
    email: UserEmailVO | None = field(default=None)
    email_verified_at: datetime | None = field(default=None)
    role: UserRoleEnum

    @classmethod
    def create_guest(
        cls,
        id: PrincipalIdVO,
    ) -> Self:
        return cls(id=id, role=UserRoleEnum.GUEST)

    @classmethod
    def create_user(
        cls,
        *,
        id: PrincipalIdVO,
        email: UserEmailVO,
        role: UserRoleEnum = UserRoleEnum.USER,
    ) -> Self:
        if role is UserRoleEnum.GUEST:
            raise VerifiedUserCannotBeGuest()
        now = get_current_dt()
        return cls(
            id=id,
            email=email,
            email_verified_at=now,
            role=role,
        )

    def attach_email(self, email: UserEmailVO) -> None:
        if self.email is not None and self.email != email:
            raise UserEmailAlreadySet()
        self.email = email
        self.email_verified_at = None

    def verify_email(self) -> None:
        if self.email is None:
            raise CannotVerifyEmailWithoutEmail()
        if self.email_verified_at is not None:
            return
        self.email_verified_at = get_current_dt()
        if self.role is UserRoleEnum.GUEST:
            self.role = UserRoleEnum.USER
