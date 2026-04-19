from dataclasses import dataclass

from app.core.domain.value_objects.id import (
    PlaceIdVO,
    RouteIdVO,
    RoutePointIdVO,
)
from app.modules.routes.domain.value_objects.point_index.object import RoutePointIndexVO


@dataclass(slots=True, kw_only=True)
class RoutePoint:
    id: RoutePointIdVO
    route_id: RouteIdVO
    place_id: PlaceIdVO
    index: RoutePointIndexVO

    @classmethod
    def create(
        cls,
        route_id: RouteIdVO,
        place_id: PlaceIdVO,
        index: RoutePointIndexVO,
    ) -> "RoutePoint":
        return cls(
            id=RoutePointIdVO.new(),
            route_id=route_id,
            place_id=place_id,
            index=index,
        )
