from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    Enum,
    ForeignKey,
    String,
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
from app.modules.places.shared.enums import PlacePhoneTypeEnum

if TYPE_CHECKING:
    from app.modules.places.infrastructure.database.models.base.place import (
        PlaceModel,
    )


class PlacePhoneModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "place_phones"
    __table_args__ = (UniqueConstraint("place_id", "number"),)

    place_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey(
            "places.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    number: Mapped[str] = mapped_column(String(20))
    type: Mapped[PlacePhoneTypeEnum] = mapped_column(
        Enum(PlacePhoneTypeEnum, name="place_phone_type_enum")
    )
    is_primary: Mapped[bool] = mapped_column(default=False)

    place: Mapped["PlaceModel"] = relationship(
        "PlaceModel",
        back_populates="phones",
    )
