from typing import Annotated

from fastapi import (
    Depends,
    Query,
)
from pydantic import (
    BaseModel,
)
from pydantic.v1 import Field


class BBoxQuery(BaseModel):
    south: float = Field(
        ...,
        description="Southern latitude of the map bounds.",
    )
    west: float = Field(
        ...,
        description="Western longitude of the map bounds.",
    )
    north: float = Field(
        ...,
        description="Northern latitude of the map bounds.",
    )
    east: float = Field(
        ...,
        description="Eastern longitude of the map bounds.",
    )


def get_bbox(
    south: Annotated[
        float,
        Query(description="Southern latitude of the map bounds."),
    ],
    west: Annotated[
        float,
        Query(description="Western longitude of the map bounds."),
    ],
    north: Annotated[
        float,
        Query(description="Northern latitude of the map bounds."),
    ],
    east: Annotated[
        float,
        Query(description="Eastern longitude of the map bounds."),
    ],
) -> BBoxQuery:
    return BBoxQuery(
        south=south,
        west=west,
        north=north,
        east=east,
    )


BBoxDep = Annotated[BBoxQuery, Depends(get_bbox)]
