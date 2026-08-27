from typing import TYPE_CHECKING

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from uuid6 import UUID

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    PKUUIDMixin,
    TimestampMixin,
)
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum

if TYPE_CHECKING:
    from app.modules.auth.infrastructure.database.models import PrincipalModel


class StaffMemberModel(PKUUIDMixin, TimestampMixin, BaseModel):
    __tablename__ = "staff_members"

    # Overrides PKUUIDMixin.id: this id is a FK to principals.id, not a
    # self-generated primary key, so it has no default.
    id: Mapped[UUID] = mapped_column(
        _UUID(),
        ForeignKey("principals.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[StaffRoleEnum] = mapped_column(
        Enum(StaffRoleEnum, name="staff_role_enum")
    )

    principal: Mapped["PrincipalModel"] = relationship(
        "PrincipalModel",
        back_populates="staff_member",
        lazy="raise",
    )
