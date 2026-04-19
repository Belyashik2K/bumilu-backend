from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import make_data_list_response_schema
from app.modules.places.presentation.api.schemas.places.examples import (
    NUMBER_EXAMPLE,
    PHONE_TYPE_EXAMPLE,
    UUID_EXAMPLE,
)
from app.modules.places.shared.enums import PlacePhoneTypeEnum


class BasePlacePhoneSchema(BaseModel):
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


class PlacePhoneSchema(BasePlacePhoneSchema): ...


class AdminPlacePhoneSchema(BasePlacePhoneSchema):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place phone number",
        examples=[UUID_EXAMPLE],
    )


class UpdatePlacePhoneSchema(BaseModel):
    number: str | None = Field(
        None, description="The phone number of the place.", examples=[NUMBER_EXAMPLE]
    )
    type: PlacePhoneTypeEnum | None = Field(
        None, description="The type of the phone number.", examples=[PHONE_TYPE_EXAMPLE]
    )


AdminPlacePhoneListResponseSchema = make_data_list_response_schema(
    item_type=AdminPlacePhoneSchema,
    description="Response schema for a list of place phone numbers for admin users",
)
