from app.core.shared.domain.value_objects.id import IdVO
from app.core.shared.exceptions.application.base import ApplicationNotFoundException
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class FavouriteEntityNotFound(ApplicationNotFoundException):
    def __init__(self, entity_type: FavouriteEntityTypeEnum, entity_id: IdVO) -> None:
        super().__init__(
            message=f"{entity_type.capitalize()} with id {entity_id} not found"
        )
