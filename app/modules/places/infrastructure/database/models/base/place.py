from typing import TYPE_CHECKING
from uuid import UUID

from geoalchemy2 import Geography
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
    from app.modules.places.infrastructure.database.models.base.category import (
        PlaceCategoryModel,
    )


class PlaceModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "places"

    category_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey(
            "place_categories.id",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
    )
    location: Mapped[object] = mapped_column(
        Geography(geometry_type="POINT", srid=4326, spatial_index=False)
    )
    timezone: Mapped[str] = mapped_column(String(64))

    category: Mapped["PlaceCategoryModel"] = relationship(
        "PlaceCategoryModel",
        back_populates="places",
    )
