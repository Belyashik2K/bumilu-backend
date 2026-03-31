from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import OffsetPaginationSchema

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
    )
    m_to_start_place: float | None = Field(
        None,
        description="Distance in meters from the user's location to the starting place of the route",
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
