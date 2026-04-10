from dataclasses import dataclass
from string import ascii_lowercase

from app.modules.places.domain.categories.value_objects.slug.exceptions import (
    InvalidSlug,
)

ALLOWED_CHARACTERS = ascii_lowercase + "-"


@dataclass(frozen=True, slots=True)
class PlaceCategorySlugVO:
    value: str

    def _is_valid_slug(self) -> bool:
        if not self.value:
            return False

        return all(char in ALLOWED_CHARACTERS for char in self.value)

    def __post_init__(self) -> None:
        if not self._is_valid_slug():
            raise InvalidSlug(slug=self.value)
