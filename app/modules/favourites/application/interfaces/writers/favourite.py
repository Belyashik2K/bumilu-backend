from abc import (
    ABC,
    abstractmethod,
)

from app.core.domain.value_objects.id import (
    IdVO,
    PrincipalIdVO,
)
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class IFavouriteWriter(ABC):
    @abstractmethod
    async def add_if_not_exists(
        self,
        user_id: PrincipalIdVO,
        entity_type: FavouriteEntityTypeEnum,
        entity_id: IdVO,
    ) -> None: ...

    @abstractmethod
    async def remove_if_exists(
        self,
        user_id: PrincipalIdVO,
        entity_type: FavouriteEntityTypeEnum,
        entity_id: IdVO,
    ) -> None: ...
