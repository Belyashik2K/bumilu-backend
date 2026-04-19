from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    ForeignKey,
    Index,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import CreatedAtMixin

if TYPE_CHECKING:
    from app.modules.places.infrastructure.database.models.base.place import PlaceModel
    from app.modules.users.infrastructure.database.models.user import UserModel


class PlaceFavouriteModel(CreatedAtMixin, BaseModel):
    __tablename__ = "place_favourites"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "place_id"),
        Index("ix_place_favourites_place_id", "place_id"),
    )

    user_id: Mapped[UUID] = mapped_column(
        _UUID,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    place_id: Mapped[UUID] = mapped_column(
        _UUID,
        ForeignKey("places.id", ondelete="CASCADE", onupdate="CASCADE"),
    )

    place: Mapped["PlaceModel"] = relationship(
        "PlaceModel", back_populates="favourites"
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="favourite_places",
    )
