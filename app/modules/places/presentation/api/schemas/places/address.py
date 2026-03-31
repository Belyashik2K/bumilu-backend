from pydantic import (
    BaseModel,
    Field,
)

DISPLAY_ADDRESS_EXAMPLE = "Saint-Petersburg, 2 Murinskiy Prospekt, 3"
TAXI_ADDRESS_EXAMPLE = "Россия, Санкт-Петербург, 2-й Муринский проспект, 3"
TAXI_COMMENT_EXAMPLE = "Подъезд сразу узнаете, там короче табличка массажки"


class PlaceAddressSchema(BaseModel):
    display: str = Field(
        ...,
        description="Formatted and localized address for displaying to users.",
        examples=[DISPLAY_ADDRESS_EXAMPLE],
    )
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
