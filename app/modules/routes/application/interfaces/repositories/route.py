from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.domain.value_objects.id import RouteIdVO
from app.modules.routes.domain.models.route.model import Route


class IRouteRepository(IBaseRepository[Route], ABC):
    @abstractmethod
    async def delete_by_id(self, route_id: RouteIdVO) -> None: ...
