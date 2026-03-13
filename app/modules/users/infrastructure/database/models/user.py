from datetime import datetime
from typing import (
    TYPE_CHECKING,
)
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    TimestampMixin,
)
from app.core.shared.enums import UserRoleEnum

if TYPE_CHECKING:
    from app.modules.chat.infrastructure.database.models import (
        ChatModel,
    )
    from app.modules.reviews.infrastructure.database.models import (
        ReviewModel,
    )

if TYPE_CHECKING:
    from app.modules.auth.infrastructure.database.models import PrincipalModel


class UserModel(TimestampMixin, BaseModel):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey("principals.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    email: Mapped[str | None] = mapped_column(unique=True)
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum, name="user_role_enum")
    )

    principal: Mapped["PrincipalModel"] = relationship(
        "PrincipalModel",
        back_populates="user",
        lazy="raise",
    )
    chats: Mapped[list["ChatModel"]] = relationship(
        "ChatModel",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="raise",
    )
    reviews: Mapped[list["ReviewModel"]] = relationship(
        "ReviewModel",
        back_populates="author",
        cascade="all, delete-orphan",
        lazy="raise",
    )
