from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PlacePhotoReadModel:
    url: str
    thumbnail_url: str
