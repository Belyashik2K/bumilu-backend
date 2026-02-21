from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    ForeignKey,
    Index,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    CreatedAtMixin,
    PKUUIDMixin,
)

if TYPE_CHECKING:
    from app.modules.auth.infrastructure.database.models import DeviceModel
    from app.modules.users.infrastructure.database.models import UserModel


class AuthSessionModel(PKUUIDMixin, CreatedAtMixin, BaseModel):
    __tablename__ = "auth_sessions"

    user_id: Mapped[UUID] = mapped_column(
        _UUID, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    device_id: Mapped[UUID] = mapped_column(
        _UUID, ForeignKey("devices.id", ondelete="CASCADE"), index=True
    )
    refresh_token_hash: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime] = mapped_column(index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(index=True)

    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="auth_sessions",
        lazy="joined",
    )
    device: Mapped["DeviceModel"] = relationship(
        "DeviceModel",
        back_populates="auth_session",
        lazy="joined",
    )

    __table_args__ = (
        Index(
            "ix_auth_sessions_user_device_revoked_at",
            "user_id",
            "device_id",
            postgresql_where=revoked_at.isnot(None),
        ),
    )
