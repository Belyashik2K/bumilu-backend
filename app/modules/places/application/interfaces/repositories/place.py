from abc import ABC

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.places.domain.places.models.place.model import Place


class IPlaceRepository(IBaseRepository[Place], ABC): ...
