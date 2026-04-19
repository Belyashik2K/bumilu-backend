from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.entity_resolver import ITargetChecker
from app.core.domain.value_objects.id import IdVO
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class IFavouriteTargetChecker(ITargetChecker, ABC):
    @abstractmethod
    async def exists(
        self,
        entity_type: FavouriteEntityTypeEnum,
        entity_id: IdVO,
    ) -> bool: ...
