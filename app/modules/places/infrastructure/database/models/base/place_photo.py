from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    Enum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    PKUUIDMixin,
    TimestampMixin,
)
from app.modules.places.shared.enums.place_photo_status import PlacePhotoStatusEnum

if TYPE_CHECKING:
    from app.modules.places.infrastructure.database.models.base.place import (
        PlaceModel,
    )


class PlacePhotoModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "place_photos"

    place_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey("places.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
    )

    file_key: Mapped[str] = mapped_column(String(1024), unique=True, index=True)
    thumbnail_file_key: Mapped[str | None] = mapped_column(String(1024))

    status: Mapped[PlacePhotoStatusEnum] = mapped_column(
        Enum(PlacePhotoStatusEnum, name="place_photo_status_enum"), index=True
    )
    original_filename: Mapped[str | None] = mapped_column(String(512))
    content_type: Mapped[str | None] = mapped_column(String(128))
    file_size: Mapped[int | None] = mapped_column()

    upload_expires_at: Mapped[datetime | None] = mapped_column()
    uploaded_at: Mapped[datetime | None] = mapped_column()
    processed_at: Mapped[datetime | None] = mapped_column()
    failed_reason: Mapped[str | None] = mapped_column(Text)

    place: Mapped[PlaceModel] = relationship(
        "PlaceModel",
        back_populates="photos",
    )
