from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceLocationReadModel:
    latitude: float
    longitude: float
