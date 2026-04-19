from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.enums import LanguageEnum
from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    PKUUIDMixin,
    TimestampMixin,
)

if TYPE_CHECKING:
    from app.modules.places.infrastructure.database.models.base.place import (
        PlaceModel,
    )


class PlaceTranslationModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "place_translations"
    __table_args__ = (UniqueConstraint("place_id", "language_code"),)

    place_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey("places.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    language_code: Mapped[LanguageEnum] = mapped_column(
        Enum(LanguageEnum, name="language_enum")
    )
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(1024))
    short_description: Mapped[str | None] = mapped_column(String(255))
    address_display: Mapped[str | None] = mapped_column(
        String(255)
    )  # TODO: make it required

    place: Mapped["PlaceModel"] = relationship(
        "PlaceModel",
        back_populates="translations",
    )
