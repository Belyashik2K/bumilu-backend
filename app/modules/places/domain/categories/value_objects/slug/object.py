from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCategorySlugVO:
    slug: str

    def _is_valid_slug(self) -> bool:
        if not self.slug:
            return False

        return self.slug.isalpha()

    def __post_init__(self) -> None:
        if not self._is_valid_slug():
            raise ValueError(f"Invalid slug: {self}")
