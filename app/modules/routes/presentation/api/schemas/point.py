from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.application.queries.places.shared.views import PlaceCardView


class RoutePointSchema(BaseModel):
    index: int = Field(
        ...,
        description="Index of the point in the route.",
    )
    preview: PlaceCardView = Field(
        ...,
        description="Preview of the place at this point.",
    )
