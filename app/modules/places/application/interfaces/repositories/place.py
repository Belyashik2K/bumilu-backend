from abc import (
    ABC,
    abstractmethod,
)

from app.core.domain.value_objects.id import PlaceIdVO
from app.modules.places.domain.places.models.place.model import Place


class IPlaceRepository(ABC):
    @abstractmethod
    async def get_by_id(self, place_id: PlaceIdVO) -> Place | None: ...

    @abstractmethod
    async def get_by_id_with_phones(self, place_id: PlaceIdVO) -> Place | None: ...

    @abstractmethod
    async def save(self, entity: Place) -> Place: ...

    @abstractmethod
    async def delete_by_id(self, place_id: PlaceIdVO) -> None: ...
