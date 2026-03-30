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

from app.core.enums import LanguageEnum
from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    PKUUIDMixin,
    TimestampMixin,
)

if TYPE_CHECKING:
    from app.modules.routes.infrastructure.database.models.base.route import (
        RouteModel,
    )


class RouteTranslationModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "route_translations"
    __table_args__ = (UniqueConstraint("route_id", "language_code"),)

    route_id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey(
            "routes.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    language_code: Mapped[LanguageEnum] = mapped_column(
        Enum(LanguageEnum, name="language_enum")
    )
    title: Mapped[str] = mapped_column(String(255))
    short_description: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(4096))

    route: Mapped["RouteModel"] = relationship(
        "RouteModel",
        back_populates="translations",
    )
