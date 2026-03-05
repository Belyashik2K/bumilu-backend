from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    VARCHAR,
    DateTime,
    Enum,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    PKUUIDMixin,
    TimestampMixin,
)
from app.core.shared.enums import LanguageEnum
from app.modules.chat.shared.enums import ChatStatusEnum


class ChatModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "chats"

    user_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
    )
    language: Mapped[LanguageEnum] = mapped_column(
        Enum(LanguageEnum, name="language_enum"),
    )
    status: Mapped[ChatStatusEnum] = mapped_column(
        Enum(ChatStatusEnum, name="chat_status_enum"),
        index=True,
    )
    last_location_latitude: Mapped[float | None] = mapped_column()
    last_location_longitude: Mapped[float | None] = mapped_column()
    last_message_preview: Mapped[str | None] = mapped_column(VARCHAR(32))
    last_activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index(
            "uq_chats_user_id_active",
            "user_id",
            unique=True,
            postgresql_where=(status != ChatStatusEnum.CLOSED),
        ),
    )
