from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.examples import (
    LATITUDE_EXAMPLE,
    LONGITUDE_EXAMPLE,
)


class PlaceLocationSchema(BaseModel):
    latitude: float = Field(
        ...,
        description="Latitude of the place location",
        examples=[LATITUDE_EXAMPLE],
    )
    longitude: float = Field(
        ...,
        description="Longitude of the place location",
        examples=[LONGITUDE_EXAMPLE],
    )
