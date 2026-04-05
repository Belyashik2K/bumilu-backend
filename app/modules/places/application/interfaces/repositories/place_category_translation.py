from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.places.domain.categories.models.category_translation.model import (
    PlaceCategoryTranslation,
)


class IPlaceCategoryTranslationRepository(
    IBaseRepository[PlaceCategoryTranslation], ABC
):
    @abstractmethod
    async def save_many(self, translations: list[PlaceCategoryTranslation]) -> None: ...
