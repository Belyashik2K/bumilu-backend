from abc import (
    ABC,
    abstractmethod,
)

from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlacePhotoIdVO,
)


class IFileKeyGenerator(ABC):
    @abstractmethod
    def generate_place_photo_key(
        self, place_id: PlaceIdVO, photo_id: PlacePhotoIdVO, content_type: str
    ) -> str: ...
