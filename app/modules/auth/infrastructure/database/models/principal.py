from sqlalchemy import Enum
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import PKUUIDMixin
from app.modules.auth.shared.enums import PrincipalTypeEnum


class PrincipalModel(PKUUIDMixin, BaseModel):
    __tablename__ = "principals"

    type: Mapped[PrincipalTypeEnum] = mapped_column(
        Enum(PrincipalTypeEnum, name="principal_type_enum"), unique=True
    )
