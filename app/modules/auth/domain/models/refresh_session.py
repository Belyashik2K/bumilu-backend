from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Self

from app.core.shared.domain.value_objects.id import (
    SessionIdVO,
    UserIdVO,
)
from app.core.shared.utils import get_current_dt


@dataclass(slots=True, kw_only=True)
class RefreshSession:
    id: SessionIdVO
    user_id: UserIdVO
    refresh_token_hash: str
    expires_at: datetime
    revoked_at: datetime | None = field(default=None)

    def revoke(self) -> None:
        if self.revoked_at is not None:
            return
        self.revoked_at = get_current_dt()

    def is_active(self) -> bool:
        return self.revoked_at is None and self.expires_at > get_current_dt()

    def revoke_if_expired(self) -> bool:
        now = get_current_dt()
        if self.revoked_at is None and self.expires_at <= now:
            self.revoked_at = now
            return True
        return False

    @classmethod
    def create(
        cls,
        user_id: UserIdVO,
        refresh_token_hash: str,
        expires_at: datetime,
    ) -> Self:
        if expires_at <= get_current_dt():
            raise ValueError("Expiration time must be in the future")

        return cls(
            id=SessionIdVO.new(),
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
        )
