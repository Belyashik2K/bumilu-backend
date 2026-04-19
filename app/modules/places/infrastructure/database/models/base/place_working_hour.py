from datetime import time
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
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
    from .place_working_day import PlaceWorkingDayModel


class PlaceWorkingHourModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "place_working_hours"
    __table_args__ = (
        CheckConstraint("start_time <> end_time", name="ck_pwh_start_end_not_equal"),
        UniqueConstraint(
            "working_day_id",
            "start_time",
            "end_time",
        ),
    )

    working_day_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey("place_working_days.id", ondelete="CASCADE"),
    )

    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)

    working_day: Mapped["PlaceWorkingDayModel"] = relationship(
        "PlaceWorkingDayModel",
        back_populates="working_hours",
    )
