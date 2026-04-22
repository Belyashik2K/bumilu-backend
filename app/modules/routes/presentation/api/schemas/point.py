from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import make_data_list_response_schema
from app.modules.places.presentation.api.schemas.places.card import (
    AdminPlaceCardSchema,
    PlaceCardSchema,
)


class BaseRoutePointSchema(BaseModel):
    index: int = Field(
        ...,
        description="Index of the point in the route.",
    )


class RoutePointSchema(BaseRoutePointSchema):
    preview: PlaceCardSchema = Field(
        ...,
        description="Preview of the place at this point.",
    )


class AdminRoutePointSchema(BaseRoutePointSchema):
    preview: AdminPlaceCardSchema = Field(
        ...,
        description="Preview of the place at this point.",
    )


class ReplaceRoutePointsRequestSchema(BaseModel):
    place_ids: list[UUID7] = Field(
        default_factory=list,
        description="Ordered list of place IDs to replace the existing points in the route.",
    )


class AddRoutePointRequestSchema(BaseModel):
    place_id: UUID7 = Field(
        ...,
        description="ID of the place to add as a point in the route.",
    )


AdminRoutePointListSchema = make_data_list_response_schema(
    item_type=AdminRoutePointSchema,
    description="List of points in the route.",
)
