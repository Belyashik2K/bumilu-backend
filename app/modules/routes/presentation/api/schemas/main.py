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


class RouteSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the route",
        examples=[UUID_EXAMPLE],
    )
    title: str = Field(
        ...,
        description="Title of the route",
        examples=[TITLE_EXAMPLE],
    )
    description: str | None = Field(
        None,
        description="Detailed description of the route",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    short_description: str | None = Field(
        None,
        description="Short description of the route",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    points: list[RoutePointSchema] = Field(
        default_factory=list,
        description="Ordered list of points included in the route, where each point represents a place",
    )
    total_points: int = Field(
        ...,
        description="Total number of points included in the route",
        examples=[5],
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
