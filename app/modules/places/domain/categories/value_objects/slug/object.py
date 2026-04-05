from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlaceCategorySlugVO:
    value: str

    def _is_valid_slug(self) -> bool:
        if not self.value:
            return False

        return self.value.isalpha()

    def __post_init__(self) -> None:
        if not self._is_valid_slug():
            raise ValueError(f"Invalid slug: {self}")
