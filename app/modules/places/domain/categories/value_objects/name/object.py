from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCategoryNameVO:
    name: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Place category name cannot be empty")
