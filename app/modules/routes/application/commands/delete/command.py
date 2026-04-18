from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRouteCommand:
    route_id: UUID
