from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
    PlaceCategoryTranslationIdVO,
)
from app.core.enums import LanguageEnum
from app.modules.places.domain.categories.models.category_translation.model import (
    PlaceCategoryTranslation,
)


class IPlaceCategoryTranslationRepository(
    IBaseRepository[PlaceCategoryTranslation], ABC
):
    @abstractmethod
    async def get_by_category_id_and_language_code(
        self, category_id: PlaceCategoryIdVO, language_code: LanguageEnum
    ) -> PlaceCategoryTranslation | None: ...

    @abstractmethod
    async def delete_by_id(
        self, translation_id: PlaceCategoryTranslationIdVO
    ) -> None: ...
