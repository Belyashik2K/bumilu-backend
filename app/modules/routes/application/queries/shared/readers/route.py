from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.enums import LanguageEnum
from app.modules.places.shared.enums.route_sort import RouteSortByEnum
from app.modules.routes.application.queries.shared.views import (
    RouteCardPage,
    RouteView,
)


class IRouteReader(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        route_id: UUID,
        *,
        translation_language: LanguageEnum,
    ) -> RouteView | None: ...

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
    ) -> RouteCardPage: ...
