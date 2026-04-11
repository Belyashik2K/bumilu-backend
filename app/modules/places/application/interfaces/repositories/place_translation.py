from abc import ABC

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.places.domain.places.models.place_translation.model import (
    PlaceTranslation,
)


class IPlaceTranslationRepository(IBaseRepository[PlaceTranslation], ABC): ...
