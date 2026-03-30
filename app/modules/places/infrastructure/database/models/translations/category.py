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
    from app.modules.places.infrastructure.database.models.base.place_category import (
        PlaceCategoryModel,
    )


class PlaceCategoryTranslationModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "place_category_translations"
    __table_args__ = (UniqueConstraint("category_id", "language_code"),)

    category_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey("place_categories.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    language_code: Mapped[LanguageEnum] = mapped_column(
        Enum(LanguageEnum, name="language_enum")
    )
    name: Mapped[str] = mapped_column(String(64))

    category: Mapped["PlaceCategoryModel"] = relationship(
        "PlaceCategoryModel",
        back_populates="translation",
    )
