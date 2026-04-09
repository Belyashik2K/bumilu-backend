from dataclasses import dataclass

from app.modules.places.domain.categories.value_objects.slug.exceptions import (
    InvalidSlug,
)


@dataclass(frozen=True, slots=True)
class PlaceCategorySlugVO:
    value: str

    def _is_valid_slug(self) -> bool:
        if not self.value:
            return False

        return self.value.isalpha()

    def __post_init__(self) -> None:
        if not self._is_valid_slug():
            raise InvalidSlug(slug=self.value)
