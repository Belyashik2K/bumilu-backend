from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.enums import LanguageEnum
from app.modules.places.shared.enums.place_category_status import (
    PlaceCategoryStatusEnum,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCategoryTranslationReadModel:
    language_code: LanguageEnum
    name: str


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCategoryReadModel:
    id: UUID
    slug: str
    icon_key: str
    marker_color: str


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalizedPlaceCategoryReadModel(PlaceCategoryReadModel):
    name: str


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminPlaceCategoryReadModel(PlaceCategoryReadModel):
    name: str | None = field(default=None)
    total_places: int = field(default=0)
    status: PlaceCategoryStatusEnum
