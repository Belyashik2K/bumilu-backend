from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import OffsetPaginationSchema
from app.modules.routes.presentation.api.schemas.point import RoutePointSchema
from app.modules.routing.shared.enums.travel_mode import TravelModeEnum

UUID_EXAMPLE = "123e4567-e89b-12d3-a456-426614174000"
TITLE_EXAMPLE = "Best massage parlors in St. Petersburg"
SHORT_DESCRIPTION_EXAMPLE = "A list of the best massage parlors in St. Petersburg, based on reviews and ratings."


class RouteCardSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place",
        examples=[UUID_EXAMPLE],
    )
    title: str = Field(
        ...,
        description="Title of the place",
        examples=[TITLE_EXAMPLE],
    )
    short_description: str | None = Field(
        None,
        description="Short description of the place",
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


class PaginatedRouteCardsResponseSchema(BaseModel):
    routes: list[RouteCardSchema] = Field(
        default_factory=list,
        description="A list of route cards matching the search criteria",
    )
    pagination: OffsetPaginationSchema = Field(
        ...,
        description="Pagination information for the retrieved route cards",
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
