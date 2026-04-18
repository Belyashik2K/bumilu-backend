from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.card import PlaceCardSchema


class RoutePointSchema(BaseModel):
    index: int = Field(
        ...,
        description="Index of the point in the route.",
    )
    preview: PlaceCardSchema = Field(
        ...,
        description="Preview of the place at this point.",
    )


class ReplaceRoutePointsRequestSchema(BaseModel):
    place_ids: list[UUID7] = Field(
        default_factory=list,
        description="Ordered list of place IDs to replace the existing points in the route.",
    )
