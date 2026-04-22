from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RemoveRoutePointCommand:
    route_id: UUID
    place_id: UUID
