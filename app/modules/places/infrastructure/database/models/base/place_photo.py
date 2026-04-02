from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    ForeignKey,
    String,
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

if TYPE_CHECKING:
    from app.modules.places.infrastructure.database.models.base.place import (
        PlaceModel,
    )


class PlacePhotoModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "place_photos"

    place_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey(
            "places.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        index=True,
    )

    file_key: Mapped[str] = mapped_column(String(1024))
    thumbnail_file_key: Mapped[str] = mapped_column(String(1024))

    place: Mapped[PlaceModel] = relationship(
        "PlaceModel",
        back_populates="photos",
    )
