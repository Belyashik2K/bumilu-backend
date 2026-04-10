from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum,
    String,
    func,
    select,
)
from sqlalchemy.orm import (
    Mapped,
    column_property,
    declared_attr,
    mapped_column,
    relationship,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    PKUUIDMixin,
    TimestampMixin,
)
from app.modules.places.infrastructure.database.models.translations.category import (
    PlaceCategoryTranslationModel,
)
from app.modules.places.shared.enums.place_category_status import (
    PlaceCategoryStatusEnum,
)

if TYPE_CHECKING:
    from app.modules.places.infrastructure.database.models.base.place import (
        PlaceModel,
    )


class PlaceCategoryModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "place_categories"

    slug: Mapped[str] = mapped_column(String(64), unique=True)
    icon_key: Mapped[str] = mapped_column(
        String(128)
    )  # Icon key for frontend from Lucide Icons (e.g. "landmark", "park", "museum")
    marker_color: Mapped[str] = mapped_column(
        String(7)
    )  # Hex color code (e.g. "#FF0000")
    status: Mapped[PlaceCategoryStatusEnum] = mapped_column(
        Enum(PlaceCategoryStatusEnum, name="place_category_status_enum"),
    )

    @declared_attr
    def translation_language_codes(self):
        return column_property(
            select(func.array_agg(PlaceCategoryTranslationModel.language_code))
            .where(PlaceCategoryTranslationModel.category_id == self.id)
            .correlate_except(PlaceCategoryTranslationModel)
            .scalar_subquery()
        )

    translations: Mapped[list["PlaceCategoryTranslationModel"]] = relationship(
        "PlaceCategoryTranslationModel",
        back_populates="category",
        cascade="all, delete-orphan",
    )
    places: Mapped[list["PlaceModel"]] = relationship(
        "PlaceModel",
        back_populates="category",
        cascade="all, delete-orphan",
    )
