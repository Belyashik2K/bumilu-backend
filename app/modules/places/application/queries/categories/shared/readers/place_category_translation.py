from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.enums import LanguageEnum
from app.modules.places.application.queries.categories.shared.models.place_category import (
    PlaceCategoryTranslationReadModel,
)


class IPlaceCategoryTranslationReader(ABC):
    @abstractmethod
    async def get_by_category_id_and_language_code(
        self,
        category_id: UUID,
        language_code: LanguageEnum,
    ) -> PlaceCategoryTranslationReadModel | None: ...

    @abstractmethod
    async def list_by_category_id(
        self,
        category_id: UUID,
    ) -> list[PlaceCategoryTranslationReadModel]: ...
