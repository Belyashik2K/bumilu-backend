from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    VARCHAR,
    DateTime,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from uuid6 import UUID

from app.core.enums import DevicePlatformEnum
from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    CreatedAtMixin,
    PKUUIDMixin,
)

if TYPE_CHECKING:
    from app.modules.auth.infrastructure.database.models import AuthSessionModel


class DeviceModel(PKUUIDMixin, CreatedAtMixin, BaseModel):
    __tablename__ = "devices"

    platform: Mapped[DevicePlatformEnum] = mapped_column(
        Enum(DevicePlatformEnum, name="device_platform_enum")
    )
    name: Mapped[str | None] = mapped_column(VARCHAR(255))
    app_version: Mapped[str] = mapped_column(VARCHAR(32))

    guest_user_id: Mapped[UUID | None] = mapped_column(
        _UUID,
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
        index=True,
    )

    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    auth_sessions: Mapped[list["AuthSessionModel"]] = relationship(
        "AuthSessionModel",
        back_populates="device",
        lazy="raise",
    )
