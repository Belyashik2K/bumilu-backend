from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Optional,
)

from sqlalchemy import (
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
from app.modules.users.shared.enums import UserRoleEnum

if TYPE_CHECKING:
    from app.modules.auth.infrastructure.database.models import InstallationModel


class UserModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "users"

    email: Mapped[str | None] = mapped_column(unique=True)
    email_verified_at: Mapped[datetime | None] = mapped_column()
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum, name="user_role_enum")
    )

    installation: Mapped[Optional["InstallationModel"]] = relationship(
        # Only for guest users, for registered users it will be None
        "InstallationModel",
        back_populates="user",
        lazy="joined",
    )
