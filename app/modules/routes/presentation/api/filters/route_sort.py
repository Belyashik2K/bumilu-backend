from typing import Annotated

from fastapi import (
    Depends,
    Query,
)
from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.shared.enums.route_sort import RouteSortByEnum


class RouteSortFilterSchema(BaseModel):
    sort_by: RouteSortByEnum | None = Field(
        None,
        description="Sorting mode for routes. If not provided, default sorting will be used.",
        examples=[RouteSortByEnum.NEAREST],
    )


def get_route_sort_filters(
    sort_by: Annotated[
        RouteSortByEnum | None,
        Query(
            description="Sorting mode for routes. If not provided, default sorting will be used.",
            examples=[RouteSortByEnum.NEAREST],
        ),
    ] = None,
) -> RouteSortFilterSchema:
    return RouteSortFilterSchema(sort_by=sort_by)


RouteSortFiltersDep = Annotated[
    RouteSortFilterSchema,
    Depends(get_route_sort_filters),
]
