from enum import (
    StrEnum,
)


class ReviewEntityTypeEnum(StrEnum):
    PLACE = "place"


class ReviewEntityPathEnum(StrEnum):
    PLACES = "places"

    @property
    def domain_name(self) -> ReviewEntityTypeEnum:
        return ReviewEntityTypeEnum(self.value[:-1])
