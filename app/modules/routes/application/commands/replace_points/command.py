from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class ReplaceRoutePointsCommand:
    route_id: UUID
    place_ids: list[UUID]
