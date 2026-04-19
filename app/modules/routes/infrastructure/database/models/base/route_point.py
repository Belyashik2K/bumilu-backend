from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    ForeignKey,
    Integer,
    UniqueConstraint,
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
    from app.modules.routes.infrastructure.database.models.base.route import (
        RouteModel,
    )


class RoutePointModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "route_points"
    __table_args__ = (UniqueConstraint("route_id", "point_index"),)

    route_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey(
            "routes.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    place_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey(
            "places.id",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
    )
    point_index: Mapped[int] = mapped_column(Integer())

    route: Mapped["RouteModel"] = relationship(
        "RouteModel",
        back_populates="points",
    )
    place: Mapped["PlaceModel"] = relationship(
        "PlaceModel",
        back_populates="route_points",
    )
