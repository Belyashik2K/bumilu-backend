from datetime import datetime

from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.routes.presentation.api.schemas.examples import (
    SHORT_DESCRIPTION_EXAMPLE,
    TITLE_EXAMPLE,
    UUID_EXAMPLE,
)
from app.modules.routes.presentation.api.schemas.point import RoutePointSchema
from app.modules.routes.shared.enums.route_status import RouteStatusEnum
from app.modules.routing.shared.enums.travel_mode import TravelModeEnum


class CreateRouteResponseSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the created route",
        examples=[UUID_EXAMPLE],
    )


class BaseRouteSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the route",
        examples=[UUID_EXAMPLE],
    )
    total_points: int = Field(
        ...,
        description="Total number of points included in the route",
        examples=[5],
    )


class RouteSchema(BaseRouteSchema):
    title: str = Field(
        ...,
        description="Title of the route",
        examples=[TITLE_EXAMPLE],
    )
    description: str = Field(
        ...,
        description="Detailed description of the route",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    short_description: str = Field(
        ...,
        description="Short description of the route",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    points: list[RoutePointSchema] = Field(
        default_factory=list,
        description="Ordered list of points included in the route, where each point represents a place",
    )


class AdminRouteSchema(BaseRouteSchema):
    title: str | None = Field(
        None,
        description="Title of the route. Can be null for unpublished routes.",
        examples=[TITLE_EXAMPLE],
    )
    status: RouteStatusEnum = Field(
        ...,
        description="Current status of the route.",
        examples=[RouteStatusEnum.PUBLISHED],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the route was created.",
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the route was last updated.",
    )


class BuildRoutePathForRouteRequestSchema(BaseModel):
    travel_mode: TravelModeEnum = Field(
        ...,
        description="Travel mode for building the route path.",
        examples=[TravelModeEnum.WALK],
    )


class ChangeRouteStatusRequestSchema(BaseModel):
    status: RouteStatusEnum = Field(
        ...,
        description="New status for the route.",
        examples=[RouteStatusEnum.PUBLISHED],
    )
