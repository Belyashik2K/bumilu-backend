from dataclasses import dataclass

from app.modules.places.domain.categories.value_objects.name.exceptions import (
    PlaceCategoryNameCannotBeEmpty,
)


@dataclass(frozen=True, slots=True)
class PlaceCategoryNameVO:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise PlaceCategoryNameCannotBeEmpty()
