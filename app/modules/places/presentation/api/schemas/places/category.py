from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.examples import (
    ICON_KEY_EXAMPLE,
    MARKER_COLOR_EXAMPLE,
    NAME_EXAMPLE,
    UUID_EXAMPLE,
)


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
    marker_color: str = Field(
        ...,
        description="The color of the marker associated with the place category, represented as a hex code.",
        examples=[MARKER_COLOR_EXAMPLE],
    )


class PlaceCardCategorySchema(BaseModel):
    name: str = Field(
        ...,
        description="The name of the category.",
        examples=[NAME_EXAMPLE],
    )
