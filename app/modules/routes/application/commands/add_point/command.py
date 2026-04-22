from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class AddRoutePointCommand:
    route_id: UUID
    place_id: UUID
