from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoutePointIndexVO:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise TypeError("Route point index must be an integer")

        if self.value < 0:
            raise ValueError("Route point index must be non-negative")
