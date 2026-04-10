from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.domain.value_objects.id import PlaceIdVO
from app.modules.places.domain.places.models.place.model import Place


class IPlaceRepository(IBaseRepository[Place], ABC):
    @abstractmethod
    async def delete_by_id(self, place_id: PlaceIdVO) -> None: ...
