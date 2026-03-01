from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    Enum,
    Index,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import CreatedAtMixin
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class FavouriteModel(CreatedAtMixin, BaseModel):
    __tablename__ = "favourites"

    user_id: Mapped[UUID] = mapped_column(_UUID, index=True)
    entity_type: Mapped[FavouriteEntityTypeEnum] = mapped_column(
        Enum(FavouriteEntityTypeEnum, name="favourite_entity_type_enum"),
        index=True,
    )
    entity_id: Mapped[UUID] = mapped_column(_UUID, index=True)

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "entity_type", "entity_id"),
        Index(
            "idx_favourites_entity",
            "entity_type",
            "entity_id",
        ),
    )
