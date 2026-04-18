from typing import TYPE_CHECKING

from sqlalchemy import Enum
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
from app.modules.routes.shared.enums.route_status import RouteStatusEnum

if TYPE_CHECKING:
    from app.modules.routes.infrastructure.database.models.base import (
        RoutePointModel,
    )
    from app.modules.routes.infrastructure.database.models.translations import (
        RouteTranslationModel,
    )


class RouteModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "routes"

    status: Mapped[RouteStatusEnum] = mapped_column(
        Enum(RouteStatusEnum, name="route_status_enum")
    )

    translations: Mapped[list["RouteTranslationModel"]] = relationship(
        "RouteTranslationModel",
        back_populates="route",
        cascade="all, delete-orphan",
    )
    points: Mapped[list["RoutePointModel"]] = relationship(
        "RoutePointModel",
        back_populates="route",
        cascade="all, delete-orphan",
    )
