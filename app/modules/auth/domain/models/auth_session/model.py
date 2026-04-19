from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Self

from app.core.domain.value_objects.id import (
    DeviceIdVO,
    PrincipalIdVO,
    SessionIdVO,
)
from app.core.utils import get_current_dt
from app.modules.auth.domain.models.auth_session.exceptions import (
    CannotRotateInactiveSession,
    SessionExpirationMustBeInFuture,
)
from app.modules.auth.shared.enums import PrincipalTypeEnum


@dataclass(slots=True, kw_only=True)
class AuthSession:
    id: SessionIdVO
    principal_id: PrincipalIdVO
    principal_type: PrincipalTypeEnum
    device_id: DeviceIdVO | None = field(default=None)
    refresh_token_hash: str
    expires_at: datetime
    revoked_at: datetime | None = field(default=None)

    def revoke(self) -> None:
        if self.revoked_at is not None:
            return
        self.revoked_at = get_current_dt()

    def is_active(self) -> bool:
        return self.revoked_at is None and self.expires_at > get_current_dt()

    def is_staff_session(self) -> bool:
        return self.principal_type == PrincipalTypeEnum.STAFF

    def is_user_session(self) -> bool:
        return self.principal_type == PrincipalTypeEnum.USER

    def rotate(
        self,
        refresh_token_hash: str,
        *,
        new_expires_at: datetime | None = None,
    ) -> None:
        if not self.is_active():
            raise CannotRotateInactiveSession()
        if refresh_token_hash == self.refresh_token_hash:
            return
        self.refresh_token_hash = refresh_token_hash
        self.expires_at = new_expires_at or self.expires_at

    @classmethod
    def create(
        cls,
        principal_id: PrincipalIdVO,
        principal_type: PrincipalTypeEnum,
        refresh_token_hash: str,
        expires_at: datetime,
        now: datetime,
        device_id: DeviceIdVO | None = None,
    ) -> Self:
        if expires_at <= now:
            raise SessionExpirationMustBeInFuture(expires_at)

        return cls(
            id=SessionIdVO.new(),
            principal_id=principal_id,
            principal_type=principal_type,
            device_id=device_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
        )
