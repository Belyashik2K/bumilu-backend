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
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    PKUUIDMixin,
    TimestampMixin,
)


class RoutePointModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "route_points"
    __table_args__ = (UniqueConstraint("route_id", "point_index"),)

    route_id: Mapped[_UUID] = mapped_column(
        _UUID(),
        ForeignKey(
            "routes.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    place_id: Mapped[_UUID] = mapped_column(
        _UUID(),
        ForeignKey(
            "places.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    point_index: Mapped[int] = mapped_column(Integer())
