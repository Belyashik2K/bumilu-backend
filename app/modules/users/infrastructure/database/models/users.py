from datetime import datetime

from sqlalchemy import (
    Enum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    PKUUIDMixin,
    TimestampMixin,
)
from app.modules.users.shared.enums import UserRoleEnum


class UserModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "users"

    email: Mapped[str | None] = mapped_column(unique=True)
    email_verified_at: Mapped[datetime | None] = mapped_column()
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum, name="user_role_enum")
    )
