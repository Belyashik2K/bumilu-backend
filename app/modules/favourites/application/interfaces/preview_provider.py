from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.enums import LanguageEnum
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class IFavouritePreviewProvider(ABC):
    supported_type: FavouriteEntityTypeEnum

    # TODO: return type should be more specific than object
    # this should return a more specific type than object, but it would require to make the interface generic
    # and it would add a lot of complexity for now, so we can keep it like this until
    # we need to support more types of entities
    @abstractmethod
    async def load_many(
        self, ids: list[UUID], translation_language: LanguageEnum
    ) -> dict[UUID, object]: ...
