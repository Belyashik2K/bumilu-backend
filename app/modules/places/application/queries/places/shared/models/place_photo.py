from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PlacePhotoReadModel:
    file_key: str
    thumbnail_file_key: str
