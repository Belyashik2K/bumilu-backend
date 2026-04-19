from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdatePlaceCategoryCommand:
    category_id: UUID
    slug: str | None = field(
        default=None
    )  # TODO: refactor as in places (set unset instead of None)
    icon_key: str | None = field(default=None)
    marker_color: str | None = field(default=None)
