from sqlalchemy import UUID as _UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from uuid6 import UUID


class PKUUIDMixin:
    id: Mapped[UUID] = mapped_column(_UUID(), primary_key=True)
