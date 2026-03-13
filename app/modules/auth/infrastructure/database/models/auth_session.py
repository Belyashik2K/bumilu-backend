from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from uuid6 import UUID

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    CreatedAtMixin,
    PKUUIDMixin,
)
from app.modules.auth.shared.enums import PrincipalTypeEnum

if TYPE_CHECKING:
    from app.modules.auth.infrastructure.database.models import DeviceModel


class AuthSessionModel(PKUUIDMixin, CreatedAtMixin, BaseModel):
    __tablename__ = "auth_sessions"

    principal_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey("principals.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
    )
    principal_type: Mapped[PrincipalTypeEnum] = mapped_column(
        Enum(PrincipalTypeEnum, name="principal_type_enum"),
        index=True,
    )
    device_id: Mapped[UUID | None] = mapped_column(
        _UUID(),
        ForeignKey("devices.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
    )
    refresh_token_hash: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), index=True
    )

    device: Mapped["DeviceModel"] = relationship(
        "DeviceModel",
        back_populates="auth_sessions",
        lazy="raise",
    )

    __table_args__ = (
        Index(
            "ix_auth_sessions_principal_type_principal_id_active",
            "principal_type",
            "principal_id",
            postgresql_where=revoked_at.is_(None),
        ),
    )
