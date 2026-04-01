from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import OffsetPaginationSchema

NAME_EXAMPLE = "Landmark"
SLUG_EXAMPLE = "landmark"
ICON_KEY_EXAMPLE = "landmark"
MARKER_COLOR_EXAMPLE = "#F59E0B"
UUID_EXAMPLE = "123e4567-e89b-12d3-a456-426614174000"


class PlaceCategorySchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="The unique identifier of the place category.",
        examples=[UUID_EXAMPLE],
    )
    slug: str = Field(
        ...,
        description="A unique slug representing the place category.",
        examples=[SLUG_EXAMPLE],
    )
    icon_key: str = Field(
        ...,
        description="The key for the icon associated with the place category.",
        examples=[ICON_KEY_EXAMPLE],
    )
    marker_color: str = Field(
        ...,
        description="The color of the marker associated with the place category, represented as a hex code.",
        examples=[MARKER_COLOR_EXAMPLE],
    )
    name: str = Field(
        ...,
        description="The localized name of the place category.",
        examples=[NAME_EXAMPLE],
    )


class PlaceCategoriesListResponseSchema(BaseModel):
    categories: list[PlaceCategorySchema] = Field(
        ...,
        description="A list of chat previews that match the specified filters and pagination parameters.",
    )
    pagination: OffsetPaginationSchema = Field(
        ...,
        description="Pagination information for the retrieved list of place categories.",
    )
