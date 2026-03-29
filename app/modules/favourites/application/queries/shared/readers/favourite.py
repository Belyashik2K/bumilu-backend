from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.modules.favourites.application.queries.get_all_by_user.view import (
    FavouritesPage,
)
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class IFavouriteReader(ABC):
    @abstractmethod
    async def get_favourites_by_user_id(
        self,
        user_id: UUID,
        limit: int | None = None,
        offset: int | None = None,
        entity_type: FavouriteEntityTypeEnum | None = None,
    ) -> FavouritesPage: ...
