from datetime import datetime

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
from app.modules.routes.shared.enums.route_status import RouteStatusEnum


class BaseRouteCardSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place",
        examples=[UUID_EXAMPLE],
    )
    total_places: int = Field(
        ...,
        description="Total number of places included in the route",
        examples=[5],
    )


class RouteCardSchema(BaseRouteCardSchema):
    title: str = Field(
        ...,
        description="Title of the route",
        examples=[TITLE_EXAMPLE],
    )
    short_description: str = Field(
        None,
        description="Short description of the route",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    m_to_start_place: float | None = Field(
        None,
        description="Distance in meters from the user's location to the starting place of the route",
        examples=[1984.1984],
    )


class AdminRouteCardSchema(BaseRouteCardSchema):
    title: str | None = Field(
        None,
        description="Title of the route",
        examples=[TITLE_EXAMPLE],
    )
    status: RouteStatusEnum = Field(
        ...,
        description="Status of the route",
        examples=[RouteStatusEnum.PUBLISHED],
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp of the route in ISO 8601 format",
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp of the route in ISO 8601 format",
    )


PaginatedRouteCardsResponseSchema = make_paginated_response_schema(
    item_type=RouteCardSchema,
    description="Response schema for a paginated list of route cards.",
)
PaginatedAdminRouteCardsResponseSchema = make_paginated_response_schema(
    item_type=AdminRouteCardSchema,
    description="Response schema for a paginated list of route cards for admin.",
)
