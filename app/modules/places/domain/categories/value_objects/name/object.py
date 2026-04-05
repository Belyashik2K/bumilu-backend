from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlaceCategoryNameVO:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Place category name cannot be empty")
