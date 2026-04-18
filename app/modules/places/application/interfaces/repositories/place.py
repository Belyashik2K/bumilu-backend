from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)

from app.core.domain.value_objects.id import PlaceIdVO
from app.modules.places.domain.places.models.place.model import Place


@dataclass(slots=True, kw_only=True, frozen=True)
class PlaceLoadOptions:
    phones: bool = field(default=False)
    working_days: bool = field(default=False)
    photos: bool = field(default=False)


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
