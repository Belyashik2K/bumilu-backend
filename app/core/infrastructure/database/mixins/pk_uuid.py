from uuid import UUID

from sqlalchemy import UUID as _UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class PKUUIDMixin:
    id: Mapped[UUID] = mapped_column(_UUID, primary_key=True)
