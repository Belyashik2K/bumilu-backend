from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    CheckConstraint,
    Enum,
    ForeignKey,
    SmallInteger,
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
from app.modules.places.shared.enums.place_working_day_status import (
    PlaceWorkingDayStatusEnum,
)

if TYPE_CHECKING:
    from app.modules.places.infrastructure.database.models.base.place import (
        PlaceModel,
    )
    from app.modules.places.infrastructure.database.models.base.place_working_hour import (
        PlaceWorkingHourModel,
    )


class PlaceWorkingDayModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "place_working_days"
    __table_args__ = (
        UniqueConstraint("place_id", "weekday"),
        CheckConstraint("weekday >= 1 AND weekday <= 7", name="ck_pwd_weekday_range"),
    )

    place_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey("places.id", onupdate="CASCADE", ondelete="CASCADE"),
    )
    weekday: Mapped[int] = mapped_column(SmallInteger)
    status: Mapped[PlaceWorkingDayStatusEnum] = mapped_column(
        Enum(PlaceWorkingDayStatusEnum, name="place_working_day_status_enum")
    )

    place: Mapped["PlaceModel"] = relationship(
        "PlaceModel",
        back_populates="working_days",
    )
    working_hours: Mapped[list["PlaceWorkingHourModel"]] = relationship(
        "PlaceWorkingHourModel",
        back_populates="working_day",
        cascade="all, delete-orphan",
    )
