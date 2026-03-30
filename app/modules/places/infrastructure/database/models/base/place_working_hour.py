from datetime import time
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    SmallInteger,
    Time,
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


class PlaceWorkingHourModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "place_working_hours"
    __table_args__ = (
        CheckConstraint("weekday >= 1 AND weekday <= 7", name="ck_pwh_weekday_range"),
        CheckConstraint("start_time <> end_time", name="ck_pwh_start_end_not_equal"),
        UniqueConstraint(
            "place_id",
            "weekday",
            "start_time",
            "end_time",
        ),
    )

    place_id: Mapped[UUID] = mapped_column(
        _UUID(), ForeignKey("places.id", ondelete="CASCADE")
    )
    weekday: Mapped[int] = mapped_column(SmallInteger)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)

    place: Mapped["PlaceModel"] = relationship(
        "PlaceModel",
        back_populates="working_hours",
    )
