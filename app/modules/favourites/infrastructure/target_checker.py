from app.core.domain.value_objects.id import IdVO
from app.modules.favourites.application.interfaces.target_checker import (
    IFavouriteTargetChecker,
)
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum
from app.modules.places.application.queries.places.shared.readers.place import (
    IPlaceReader,
)


class FavouriteTargetChecker(IFavouriteTargetChecker):
    def __init__(self, place_reader: IPlaceReader) -> None:
        self.mapped_readers = {
            FavouriteEntityTypeEnum.PLACE: place_reader,
        }

    async def exists(
        self,
        entity_type: FavouriteEntityTypeEnum,
        entity_id: IdVO,
    ) -> bool:
        reader = self.mapped_readers.get(entity_type)
        if not reader:
            raise ValueError(f"No reader found for entity type {entity_type}")

        return await reader.exists(entity_id.value)
