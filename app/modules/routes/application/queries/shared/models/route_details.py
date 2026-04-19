from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import UUID

from app.modules.routes.application.queries.shared.models.route_point import (
    RoutePointReadModel,
)
from app.modules.routes.shared.enums.route_status import RouteStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseRouteDetailsReadModel:
    id: UUID
    total_points: int


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteDetailsReadModel(BaseRouteDetailsReadModel):
    title: str
    description: str
    short_description: str
    points: list[RoutePointReadModel] = field(default_factory=list)


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminRouteDetailsReadModel(BaseRouteDetailsReadModel):
    title: str | None = field(default=None)
    status: RouteStatusEnum
    created_at: datetime
    updated_at: datetime
