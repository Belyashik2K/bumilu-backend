from typing import TYPE_CHECKING

from sqlalchemy import String
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
    from app.modules.places.infrastructure.database.models.translations.category_translations import (
        PlaceCategoryTranslationModel,
    )


class PlaceCategoryModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "place_categories"

    slug: Mapped[str] = mapped_column(String(64), unique=True)
    icon_key: Mapped[str] = mapped_column(String(128))

    translations: Mapped[list["PlaceCategoryTranslationModel"]] = relationship(
        "PlaceCategoryTranslationModel",
        back_populates="category",
        cascade="all, delete-orphan",
    )
