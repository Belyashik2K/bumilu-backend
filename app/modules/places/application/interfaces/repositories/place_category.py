from abc import ABC

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.places.domain.categories.models.category.model import PlaceCategory


class IPlaceCategoryRepository(IBaseRepository[PlaceCategory], ABC): ...
