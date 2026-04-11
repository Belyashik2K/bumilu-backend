from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.examples import (
    NUMBER_EXAMPLE,
    PHONE_TYPE_EXAMPLE,
)
from app.modules.places.shared.enums import PlacePhoneTypeEnum


class PlacePhoneSchema(BaseModel):
    number: str = Field(
        ..., description="The phone number of the place.", examples=[NUMBER_EXAMPLE]
    )
    type: PlacePhoneTypeEnum = Field(
        ..., description="The type of the phone number.", examples=[PHONE_TYPE_EXAMPLE]
    )
    primary: bool = Field(
        ...,
        description="Whether this phone number is the primary contact number for the place.",
        examples=[True],
    )


class UpdatePlacePhoneSchema(BaseModel):
    number: str | None = Field(
        None, description="The phone number of the place.", examples=[NUMBER_EXAMPLE]
    )
    type: PlacePhoneTypeEnum | None = Field(
        None, description="The type of the phone number.", examples=[PHONE_TYPE_EXAMPLE]
    )
