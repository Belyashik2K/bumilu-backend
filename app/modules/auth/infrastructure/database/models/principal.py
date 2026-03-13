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
from app.core.infrastructure.database.mixins import PKUUIDMixin
from app.modules.auth.shared.enums import PrincipalTypeEnum
from app.modules.staff.infrastructure.database.models import StaffMemberModel

if TYPE_CHECKING:
    from app.modules.auth.infrastructure.database.models import AuthSessionModel
    from app.modules.users.infrastructure.database.models import UserModel


class PrincipalModel(PKUUIDMixin, BaseModel):
    __tablename__ = "principals"

    type: Mapped[PrincipalTypeEnum] = mapped_column(
        Enum(PrincipalTypeEnum, name="principal_type_enum"),
        index=True,
    )

    auth_sessions: Mapped[list["AuthSessionModel"]] = relationship(
        "AuthSessionModel",
        back_populates="principal",
        cascade="all, delete-orphan",
        lazy="raise",
    )
    user: Mapped[Optional["UserModel"]] = relationship(
        "UserModel",
        back_populates="principal",
        lazy="raise",
    )
    staff_member: Mapped[Optional["StaffMemberModel"]] = relationship(
        "StaffMemberModel",
        back_populates="principal",
        lazy="raise",
    )
