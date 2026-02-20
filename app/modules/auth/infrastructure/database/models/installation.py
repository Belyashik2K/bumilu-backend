from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as _UUID,
)
from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.infrastructure.database import BaseModel
from app.core.infrastructure.database.mixins import (
    CreatedAtMixin,
    MetadataMixin,
)

if TYPE_CHECKING:
    from app.modules.users.infrastructure.database.models.users import UserModel


class InstallationModel(CreatedAtMixin, MetadataMixin, BaseModel):
    __tablename__ = "installations"

    installation_id: Mapped[UUID] = mapped_column(_UUID, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        _UUID, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )

    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="installation",
        lazy="joined",
    )
