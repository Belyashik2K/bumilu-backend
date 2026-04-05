from abc import (
    ABC,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.places.domain.categories.models.category_translation.model import (
    PlaceCategoryTranslation,
)


class IPlaceCategoryTranslationRepository(
    IBaseRepository[PlaceCategoryTranslation], ABC
): ...
