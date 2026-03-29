from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.entity_resolver import IEntityResolver
from app.core.domain.value_objects.id import IdVO
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class IFavouriteEntityResolver(IEntityResolver, ABC):
    @abstractmethod
    async def resolve(
        self,
        entity_type: FavouriteEntityTypeEnum,
        entity_id: IdVO,
    ) -> bool: ...
