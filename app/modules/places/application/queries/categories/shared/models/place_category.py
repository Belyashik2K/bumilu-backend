from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCategoryReadModel:
    id: UUID
    slug: str
    icon_key: str
    marker_color: str


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalizedPlaceCategoryReadModel(PlaceCategoryReadModel):
    name: str
