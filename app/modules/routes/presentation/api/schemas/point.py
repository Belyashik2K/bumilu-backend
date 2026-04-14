from pydantic import (
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
