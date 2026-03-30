from abc import (
    ABC,
    abstractmethod,
)

from app.core.enums import LanguageEnum
from app.modules.places.application.queries.categories.shared.views import (
    PlaceCategoriesPage,
)


class IPlaceCategoryReader(ABC):
    @abstractmethod
    async def list(
        self,
        limit: int,
        offset: int,
        translation_language: LanguageEnum,
    ) -> PlaceCategoriesPage: ...
