from dataclasses import (
    dataclass,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceTranslationReadModel:
    title: str
    description: str
    short_description: str
    display_address: str
