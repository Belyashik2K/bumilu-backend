from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.places.application.commands.categories.shared.dtos import (
    NewPlaceCategoryTranslation,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceCategoryCommand:
    slug: str
    icon_key: str
    marker_color: str
    translations: list[NewPlaceCategoryTranslation] = field(default_factory=list)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceCategoryCommandResult:
    id: UUID
