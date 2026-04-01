from typing import TYPE_CHECKING
from uuid import UUID

from geoalchemy2 import (
    Geography,
    WKBElement,
)
from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    Float,
    ForeignKey,
    String,
    and_,
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
from app.modules.reviews.infrastructure.database.models import ReviewModel
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum
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
    location: Mapped[WKBElement] = mapped_column(
        Geography(geometry_type="POINT", srid=4326, spatial_index=False)
    )
    timezone: Mapped[str] = mapped_column(String(64))
    address_taxi: Mapped[str | None] = mapped_column(String(255))
    address_taxi_comment: Mapped[str | None] = mapped_column(String(255))

    @declared_attr
    def rating_average(self):
        return column_property(
            select(func.avg(ReviewModel.rating).cast(Float))
            .where(
                and_(
                    ReviewModel.entity_id == self.id,
                    ReviewModel.entity_type == ReviewEntityTypeEnum.PLACE,
                )
            )
            .correlate_except(ReviewModel)
            .scalar_subquery()
        )

    @declared_attr
    def rating_reviews_count(self):
        return column_property(
            select(func.count(ReviewModel.id))
            .where(
                and_(
                    ReviewModel.entity_id == self.id,
                    ReviewModel.entity_type == ReviewEntityTypeEnum.PLACE,
                )
            )
            .correlate_except(ReviewModel)
            .scalar_subquery()
        )

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
