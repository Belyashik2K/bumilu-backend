from abc import (
    ABC,
    abstractmethod,
)

from app.modules.routes.application.queries.shared.views import RouteCardPage


class IRouteReader(ABC):
    @abstractmethod
    async def get_all(
        self,
        *,
        translation_language: str,
        limit: int,
        offset: int,
        latitude: float | None = None,
        longitude: float | None = None,
        sort_by: str | None = None,
    ) -> RouteCardPage: ...
