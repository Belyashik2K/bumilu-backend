from datetime import datetime

from sqlalchemy import (
    DateTime,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.shared.utils import get_current_dt


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=get_current_dt,
        server_default=func.now(),
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=get_current_dt,
        onupdate=get_current_dt,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin):
    pass
