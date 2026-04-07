from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteBounds:
    north: float
    south: float
    east: float
    west: float
