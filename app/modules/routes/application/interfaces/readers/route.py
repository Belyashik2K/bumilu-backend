from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.places.shared.enums.route_sort import RouteSortByEnum
from app.modules.routes.application.queries.shared.models.route_card import (
    AdminRouteCardReadModel,
    RouteCardReadModel,
)
from app.modules.routes.application.queries.shared.models.route_details import (
    AdminRouteDetailsReadModel,
    RouteDetailsReadModel,
)
from app.modules.routes.application.queries.shared.models.route_point import (
    AdminRoutePointReadModel,
    RouteWaypointModel,
)


class IRouteReader(ABC):
    @abstractmethod
    async def exists(self, route_id: UUID) -> bool: ...

    @abstractmethod
    async def get_by_id(
        self,
        route_id: UUID,
        *,
        translation_language: LanguageEnum,
    ) -> RouteDetailsReadModel | None: ...

    @abstractmethod
    async def get_admin_by_id(
        self,
        route_id: UUID,
        *,
        optional_translation_language: LanguageEnum,
    ) -> AdminRouteDetailsReadModel | None: ...

    @abstractmethod
    async def count_by_place_id(self, place_id: UUID) -> int: ...

    @abstractmethod
    async def get_route_waypoints(
        self,
        route_id: UUID,
    ) -> list[RouteWaypointModel]: ...

    @abstractmethod
    async def get_admin_route_points(
        self,
        route_id: UUID,
        optional_translation_language: LanguageEnum,
    ) -> list[AdminRoutePointReadModel]: ...

    @abstractmethod
    async def get_all(
        self,
        *,
        translation_language: LanguageEnum,
        limit: int,
        offset: int,
        latitude: float | None = None,
        longitude: float | None = None,
        sort_by: RouteSortByEnum | None = None,
    ) -> PageReadModel[RouteCardReadModel]: ...

    @abstractmethod
    async def admin_get_all(
        self,
        *,
        optional_translation_language: LanguageEnum,
        limit: int,
        offset: int,
    ) -> PageReadModel[AdminRouteCardReadModel]: ...
