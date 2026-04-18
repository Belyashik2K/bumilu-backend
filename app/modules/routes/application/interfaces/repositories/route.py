from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)

from app.core.domain.value_objects.id import RouteIdVO
from app.modules.routes.domain.models.route.model import Route


@dataclass(slots=True, kw_only=True, frozen=True)
class RouteLoadOptions:
    translations: bool = field(default=False)
    points: bool = field(default=False)


class IRouteRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        route_id: RouteIdVO,
        *,
        options: RouteLoadOptions | None = None,
    ) -> Route | None: ...

    @abstractmethod
    async def save(self, entity: Route) -> Route: ...

    @abstractmethod
    async def delete_by_id(self, route_id: RouteIdVO) -> None: ...
