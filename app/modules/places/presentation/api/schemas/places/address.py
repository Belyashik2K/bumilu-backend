from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.examples import (
    DISPLAY_ADDRESS_EXAMPLE,
    TAXI_ADDRESS_EXAMPLE,
    TAXI_COMMENT_EXAMPLE,
)


class BasePlaceAddressSchema(BaseModel):
    taxi: str | None = Field(
        None,
        description="Address formatted for taxi services.",
        examples=[TAXI_ADDRESS_EXAMPLE],
    )
    taxi_comment: str | None = Field(
        None,
        description="Additional comments for taxi drivers.",
        examples=[TAXI_COMMENT_EXAMPLE],
    )


class PlaceAddressSchema(BasePlaceAddressSchema):
    display: str = Field(
        ...,
        description="Formatted and localized address for displaying to users.",
        examples=[DISPLAY_ADDRESS_EXAMPLE],
    )


class AdminPlaceAddressSchema(BasePlaceAddressSchema): ...
