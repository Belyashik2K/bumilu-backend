from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

UUID_EXAMPLE = "123e4567-e89b-12d3-a456-426614174000"
NAME_EXAMPLE = "What they don't talk about in polite society"
ICON_KEY_EXAMPLE = "unknown"


class PlaceMapPOICategorySchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="The unique identifier of the category.",
        examples=[UUID_EXAMPLE],
    )
    name: str = Field(
        ...,
        description="The name of the category.",
        examples=[NAME_EXAMPLE],
    )
    icon_key: str = Field(
        ...,
        description="The key of the category icon.",
        examples=[ICON_KEY_EXAMPLE],
    )


class PlaceCardCategorySchema(BaseModel):
    name: str = Field(
        ...,
        description="The name of the category.",
        examples=[NAME_EXAMPLE],
    )
