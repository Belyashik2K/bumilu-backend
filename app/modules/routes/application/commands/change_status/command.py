from dataclasses import dataclass
from uuid import UUID

from app.modules.routes.shared.enums.route_status import RouteStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeRouteStatusCommand:
    route_id: UUID
    status: RouteStatusEnum
