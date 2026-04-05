from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.places.application.commands.categories.shared.dtos import (
    NewCategoryTranslation,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceCategoryCommand:
    slug: str
    icon_key: str
    marker_color: str
    translations: list[NewCategoryTranslation] = field(default_factory=list)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceCategoryCommandResult:
    id: UUID
