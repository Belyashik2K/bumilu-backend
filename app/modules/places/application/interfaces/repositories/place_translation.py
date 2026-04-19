from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlaceTranslationIdVO,
)
from app.core.enums import LanguageEnum
from app.modules.places.domain.places.models.place_translation.model import (
    PlaceTranslation,
)


class IPlaceTranslationRepository(IBaseRepository[PlaceTranslation], ABC):
    @abstractmethod
    async def get_by_place_id_and_language_code(
        self, place_id: PlaceIdVO, language_code: LanguageEnum
    ) -> PlaceTranslation | None: ...

    @abstractmethod
    async def delete_by_id(self, translation_id: PlaceTranslationIdVO) -> None: ...
