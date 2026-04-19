from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.application.queries.pagination import PageReadModel
from app.modules.favourites.application.queries.shared.models.favourite_record import (
    RawFavouriteRecordReadModel,
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
    ) -> PageReadModel[RawFavouriteRecordReadModel]: ...
