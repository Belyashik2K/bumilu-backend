from abc import (
    ABC,
    abstractmethod,
)

from app.core.enums import LanguageEnum
from app.modules.favourites.application.queries.shared.models.favourite_record import (
    FavouriteRecordReadModel,
    RawFavouriteRecordReadModel,
)


class IFavouritePreviewEnricher(ABC):
    @abstractmethod
    async def enrich(
        self,
        items: list[RawFavouriteRecordReadModel],
        translation_language: LanguageEnum,
    ) -> list[FavouriteRecordReadModel]: ...
