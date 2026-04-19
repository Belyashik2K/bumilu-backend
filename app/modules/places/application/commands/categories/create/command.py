from dataclasses import (
    dataclass,
)
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceCategoryCommand:
    slug: str
    icon_key: str
    marker_color: str


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceCategoryCommandResult:
    id: UUID
