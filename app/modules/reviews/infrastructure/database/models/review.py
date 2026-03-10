from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    VARCHAR,
    CheckConstraint,
    Enum,
    ForeignKey,
    Index,
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
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum

if TYPE_CHECKING:
    from app.modules.users.infrastructure.database.models import UserModel


class ReviewModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "reviews"

    author_id: Mapped[UUID] = mapped_column(
        _UUID,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
    )
    entity_type: Mapped[ReviewEntityTypeEnum] = mapped_column(
        Enum(ReviewEntityTypeEnum, name="review_entity_type_enum"),
        index=True,
    )
    entity_id: Mapped[UUID] = mapped_column(_UUID, index=True)
    text: Mapped[str | None] = mapped_column(VARCHAR(1000))
    rating: Mapped[int] = mapped_column()

    author: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="reviews", lazy="raise"
    )

    __table_args__ = (
        Index(
            "ix_reviews_entity",
            "entity_type",
            "entity_id",
        ),
        UniqueConstraint(
            "entity_type", "entity_id", "author_id", name="uq_reviews_entity_author"
        ),
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_reviews_rating_range"),
    )
