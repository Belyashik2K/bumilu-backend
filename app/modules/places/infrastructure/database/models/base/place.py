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
from app.modules.routes.infrastructure.database.models.base.route_point import (
    RoutePointModel,
)

if TYPE_CHECKING:
    from app.modules.places.infrastructure.database.models.base.place_category import (
        PlaceCategoryModel,
    )
    from app.modules.places.infrastructure.database.models.base.place_phone import (
        PlacePhoneModel,
    )
    from app.modules.places.infrastructure.database.models.base.place_working_hour import (
        PlaceWorkingHourModel,
    )
    from app.modules.places.infrastructure.database.models.translations.place import (
        PlaceTranslationModel,
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
    address_taxi: Mapped[str | None] = mapped_column(String(255))
    address_taxi_comment: Mapped[str | None] = mapped_column(String(255))

    category: Mapped["PlaceCategoryModel"] = relationship(
        "PlaceCategoryModel",
        back_populates="places",
    )
    translations: Mapped[list["PlaceTranslationModel"]] = relationship(
        "PlaceTranslationModel",
        back_populates="place",
        cascade="all, delete-orphan",
    )
    phones: Mapped[list["PlacePhoneModel"]] = relationship(
        "PlacePhoneModel",
        back_populates="place",
        cascade="all, delete-orphan",
    )
    working_hours: Mapped[list["PlaceWorkingHourModel"]] = relationship(
        "PlaceWorkingHourModel",
        back_populates="place",
        cascade="all, delete-orphan",
    )
    route_points: Mapped[list["RoutePointModel"]] = relationship(
        "RoutePointModel",
        back_populates="place",
        cascade="all, delete-orphan",
    )
