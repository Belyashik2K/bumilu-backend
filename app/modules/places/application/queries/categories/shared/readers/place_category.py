from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
)


class IPlaceCategoryReader(ABC):
    @abstractmethod
    async def exists(self, slug: str) -> bool: ...

    @abstractmethod
    async def list(
        self,
        limit: int,
        offset: int,
        translation_language: LanguageEnum,
    ) -> PageReadModel[LocalizedPlaceCategoryReadModel]: ...
