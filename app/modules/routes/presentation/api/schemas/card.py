from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import make_paginated_response_schema
from app.modules.routes.presentation.api.schemas.examples import (
    SHORT_DESCRIPTION_EXAMPLE,
    TITLE_EXAMPLE,
    UUID_EXAMPLE,
)


class RouteCardSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place",
        examples=[UUID_EXAMPLE],
    )
    title: str = Field(
        ...,
        description="Title of the route",
        examples=[TITLE_EXAMPLE],
    )
    short_description: str | None = Field(
        None,
        description="Short description of the route",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    total_places: int = Field(
        ...,
        description="Total number of places included in the route",
        examples=[5],
    )
    m_to_start_place: float | None = Field(
        None,
        description="Distance in meters from the user's location to the starting place of the route",
        examples=[1984.1984],
    )


PaginatedRouteCardsResponseSchema = make_paginated_response_schema(
    item_type=RouteCardSchema,
    description="Response schema for a paginated list of route cards.",
)
