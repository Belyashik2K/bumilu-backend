from app.core.domain.value_objects.id import IdVO
from app.modules.favourites.application.interfaces.entity_resolver import (
    IFavouriteEntityResolver,
)
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class FavouriteEntityResolver(IFavouriteEntityResolver):
    async def resolve(
        self,
        entity_type: FavouriteEntityTypeEnum,
        entity_id: IdVO,
    ) -> bool:
        return True  # TODO: Implement actual logic, when other services are implemented
