from typing import Annotated

from fastapi import (
    Depends,
    Query,
)
from pydantic import (
    BaseModel,
)


class BBoxQuery(BaseModel):
    south: float
    west: float
    north: float
    east: float


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
