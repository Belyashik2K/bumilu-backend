from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    Enum,
    ForeignKey,
    Text,
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
from app.modules.chat.shared.enums import AuthorTypeEnum


class ChatMessageModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "chat_messages"

    # TODO: VARCHAR -> String and _UUID -> _UUID() in all other models
    # TODO: Transfer length to shared constants
    chat_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey("chats.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
    )
    author_type: Mapped[AuthorTypeEnum] = mapped_column(
        Enum(AuthorTypeEnum, name="author_type_enum")
    )
    author_id: Mapped[UUID | None] = mapped_column(_UUID())
    text: Mapped[str] = mapped_column(Text())
    location_latitude: Mapped[float | None] = mapped_column()
    location_longitude: Mapped[float | None] = mapped_column()
