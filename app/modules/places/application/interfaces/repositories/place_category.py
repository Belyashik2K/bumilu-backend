from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.domain.value_objects.id import PlaceCategoryIdVO
from app.modules.places.domain.categories.models.category.model import PlaceCategory
from app.modules.places.domain.categories.value_objects.slug import PlaceCategorySlugVO


class IPlaceCategoryRepository(IBaseRepository[PlaceCategory], ABC):
    @abstractmethod
    async def get_by_slug(self, slug: PlaceCategorySlugVO) -> PlaceCategory | None: ...

    @abstractmethod
    async def delete_by_id(self, category_id: PlaceCategoryIdVO) -> None: ...
