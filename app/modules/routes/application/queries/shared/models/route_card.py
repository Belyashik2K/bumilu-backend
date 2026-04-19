from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import UUID

from app.modules.routes.shared.enums.route_status import RouteStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseRouteCardReadModel:
    id: UUID
    total_places: int


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteCardReadModel(BaseRouteCardReadModel):
    title: str
    short_description: str
    m_to_start_place: int | None = field(default=None)


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminRouteCardReadModel(BaseRouteCardReadModel):
    title: str | None = field(default=None)
    status: RouteStatusEnum
    created_at: datetime
    updated_at: datetime
