from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from app.core.domain.value_objects.id import PlaceIdVO
from app.modules.places.domain.places.models.place.model import Place


@dataclass(slots=True, kw_only=True, frozen=True)
class PlaceLoadOptions:
    phones: bool = False
    working_days: bool = False
    photos: bool = False


class IPlaceRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        place_id: PlaceIdVO,
        *,
        options: PlaceLoadOptions | None = None,
    ) -> Place | None: ...

    @abstractmethod
    async def save(self, entity: Place) -> Place: ...

    @abstractmethod
    async def delete_by_id(self, place_id: PlaceIdVO) -> None: ...
