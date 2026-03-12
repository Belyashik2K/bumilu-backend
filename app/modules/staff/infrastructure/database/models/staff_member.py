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
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


class StaffMemberModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "staff_members"

    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[StaffRoleEnum] = mapped_column(
        Enum(StaffRoleEnum, name="staff_role_enum")
    )
