from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.routes.application.queries.shared.models.route_translation import (
    RouteTranslationReadModel,
)


class IRouteTranslationReader(ABC):
    @abstractmethod
    async def get_by_route_id_and_language_code(
        self,
        route_id: UUID,
        language_code: LanguageEnum,
    ) -> RouteTranslationReadModel | None: ...

    @abstractmethod
    async def list_by_route_id(
        self,
        route_id: UUID,
        limit: int,
        offset: int,
    ) -> PageReadModel[RouteTranslationReadModel]: ...
