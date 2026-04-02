from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteCardReadModel:
    id: UUID
    title: str
    short_description: str | None = field(default=None)
    total_places: int
    m_to_start_place: int | None = field(default=None)
