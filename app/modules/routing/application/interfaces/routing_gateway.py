from abc import (
    ABC,
    abstractmethod,
)

from app.modules.routing.application.models.route_path import RoutePath
from app.modules.routing.application.queries.get_route.query import Waypoint
from app.modules.routing.shared.enums.travel_mode import TravelModeEnum


class IRoutingGateway(ABC):
    @abstractmethod
    async def get_route(
        self,
        points: list[Waypoint],
        mode: TravelModeEnum,
    ) -> RoutePath: ...
