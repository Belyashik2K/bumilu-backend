from typing import Annotated

from fastapi import (
    Depends,
    Query,
)
from pydantic import (
    BaseModel,
    Field,
)


class LocationQuery(BaseModel):
    latitude: float | None = Field(
        None,
        description="Latitude of the user location.",
    )
    longitude: float | None = Field(
        None,
        description="Longitude of the user location.",
    )


def get_location(
    latitude: Annotated[
        float | None,
        Query(description="Latitude of the user location."),
    ] = None,
    longitude: Annotated[
        float | None,
        Query(description="Longitude of the user location."),
    ] = None,
) -> LocationQuery:
    return LocationQuery(
        latitude=latitude,
        longitude=longitude,
    )


LocationDep = Annotated[LocationQuery, Depends(get_location)]
