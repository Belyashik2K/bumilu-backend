from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Self

from app.core.shared.domain.value_objects.id import (
    DeviceIdVO,
    SessionIdVO,
    UserIdVO,
)
from app.core.shared.utils import get_current_dt


@dataclass(slots=True, kw_only=True)
class AuthSession:
    id: SessionIdVO
    user_id: UserIdVO
    device_id: DeviceIdVO
    refresh_token_hash: str
    expires_at: datetime
    revoked_at: datetime | None = field(default=None)

    def revoke(self) -> None:
        if self.revoked_at is not None:
            return
        self.revoked_at = get_current_dt()

    def is_active(self) -> bool:
        return self.revoked_at is None and self.expires_at > get_current_dt()

    def rotate(
        self,
        refresh_token_hash: str,
    ) -> None:
        if not self.is_active():
            raise ValueError("Cannot rotate a revoked or expired session")
        if refresh_token_hash == self.refresh_token_hash:
            return
        self.refresh_token_hash = refresh_token_hash

    @classmethod
    def create(
        cls,
        user_id: UserIdVO,
        device_id: DeviceIdVO,
        refresh_token_hash: str,
        expires_at: datetime,
    ) -> Self:
        if expires_at <= get_current_dt():
            raise ValueError("Expiration time must be in the future")

        return cls(
            id=SessionIdVO.new(),
            user_id=user_id,
            device_id=device_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
        )
