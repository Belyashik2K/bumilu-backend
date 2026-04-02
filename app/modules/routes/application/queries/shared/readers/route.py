from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.places.shared.enums.route_sort import RouteSortByEnum
from app.modules.routes.application.queries.shared.models.route_card import (
    RouteCardReadModel,
)
from app.modules.routes.application.queries.shared.models.route_details import (
    RouteDetailsReadModel,
)


class IRouteReader(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        route_id: UUID,
        *,
        translation_language: LanguageEnum,
    ) -> RouteDetailsReadModel | None: ...

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
