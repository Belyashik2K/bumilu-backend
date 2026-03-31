from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.shared.enums import PlacePhoneTypeEnum

NUMBER_EXAMPLE = "+79999991984"
PHONE_TYPE_EXAMPLE = PlacePhoneTypeEnum.MOBILE


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
