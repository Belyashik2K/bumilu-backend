from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlacePhotoIdVO,
)
from app.modules.places.application.interfaces.file_key_generator import (
    IFileKeyGenerator,
)

_CONTENT_TYPE_TO_EXTENSION = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
}


class FileKeyGenerator(IFileKeyGenerator):
    @classmethod
    def _get_extension_from_content_type(cls, content_type: str) -> str:
        content_type = content_type.split(";")[0].strip()

        extension = _CONTENT_TYPE_TO_EXTENSION.get(content_type)
        if extension is None:
            raise ValueError(f"Unsupported content type: {content_type}")

        return extension

    def generate_place_photo_key(
        self,
        place_id: PlaceIdVO,
        photo_id: PlacePhotoIdVO,
        content_type: str,
    ) -> str:
        extension = self._get_extension_from_content_type(content_type)

        return f"places/{place_id.value}/photos/{photo_id.value}/original{extension}"
