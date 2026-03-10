from datetime import datetime
from typing import (
    TYPE_CHECKING,
)

from sqlalchemy import (
    DateTime,
    Enum,
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
from app.core.shared.enums import UserRoleEnum

if TYPE_CHECKING:
    from app.modules.auth.infrastructure.database.models import (
        AuthSessionModel,
    )
    from app.modules.chat.infrastructure.database.models import (
        ChatModel,
    )
    from app.modules.reviews.infrastructure.database.models import (
        ReviewModel,
    )


class UserModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "users"

    email: Mapped[str | None] = mapped_column(unique=True)
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum, name="user_role_enum")
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
    auth_sessions: Mapped[list["AuthSessionModel"]] = relationship(
        "AuthSessionModel",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="raise",
    )
