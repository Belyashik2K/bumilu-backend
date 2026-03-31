from pydantic import (
    BaseModel,
    Field,
)

LATITUDE_EXAMPLE = 60.002598
LONGITUDE_EXAMPLE = 30.330861


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
