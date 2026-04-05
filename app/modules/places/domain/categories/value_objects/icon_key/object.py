from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlaceCategoryIconKeyVO:
    key: str
