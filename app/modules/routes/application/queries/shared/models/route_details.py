from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.routes.application.queries.shared.models.route_point import (
    RoutePointReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteDetailsReadModel:
    id: UUID
    title: str
    description: str | None = field(default=None)
    short_description: str | None = field(default=None)
    points: list[RoutePointReadModel] = field(default_factory=list)
    total_points: int
