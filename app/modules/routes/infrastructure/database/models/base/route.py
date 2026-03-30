from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    relationship,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    PKUUIDMixin,
    TimestampMixin,
)

if TYPE_CHECKING:
    from app.modules.routes.infrastructure.database.models.translations import (
        RouteTranslationModel,
    )


class RouteModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "routes"

    translations: Mapped["RouteTranslationModel"] = relationship(
        "RouteTranslationModel",
        back_populates="route",
        cascade="all, delete-orphan",
    )
