from dataclasses import dataclass
from uuid import UUID

from app.core.application.queries.language import LanguageMixin
from app.modules.routing.shared.enums.travel_mode import TravelModeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class BuildAdminRoutePathForRouteQuery(LanguageMixin):
    route_id: UUID
    travel_mode: TravelModeEnum
