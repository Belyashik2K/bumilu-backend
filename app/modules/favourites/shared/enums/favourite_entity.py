from enum import StrEnum


class FavouriteEntityTypeEnum(StrEnum):
    PLACE = "place"


class FavouriteEntityPathEnum(StrEnum):
    PLACES = "places"

    @property
    def domain_name(self) -> FavouriteEntityTypeEnum:
        return FavouriteEntityTypeEnum(self.value[:-1])
