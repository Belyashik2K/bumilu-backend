from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import (
    make_paginated_response_schema,
)
from app.modules.places.presentation.api.schemas.categories.examples import (
    ICON_KEY_EXAMPLE,
    MARKER_COLOR_EXAMPLE,
    NAME_EXAMPLE,
    SLUG_EXAMPLE,
    UUID_EXAMPLE,
)
from app.modules.places.presentation.api.schemas.categories.translation import (
    PlaceCategoryTranslationSchema,
)


class CreatePlaceCategoryRequestSchema(BaseModel):
    slug: str = Field(
        ...,
        description="Unique slug for the place category",
        examples=[SLUG_EXAMPLE],
    )
    icon_key: str = Field(
        ...,
        description="Icon key for frontend from Lucide Icons",
        examples=[ICON_KEY_EXAMPLE],
    )
    marker_color: str = Field(
        ...,
        description="Hex color code for the marker",
        examples=[MARKER_COLOR_EXAMPLE],
    )
    translations: list[PlaceCategoryTranslationSchema] = Field(
        ...,
        description="List of translations for the place category",
    )


class CreatePlaceCategoryResponseSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="ID of the created place category",
        examples=[UUID_EXAMPLE],
    )


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


class UpdatePlaceCategoryRequestSchema(BaseModel):
    slug: str | None = Field(
        None,
        description="New unique slug for the place category",
        examples=[SLUG_EXAMPLE],
    )
    icon_key: str | None = Field(
        None,
        description="New icon key for frontend from Lucide Icons",
        examples=[ICON_KEY_EXAMPLE],
    )
    marker_color: str | None = Field(
        None,
        description="New hex color code for the marker",
        examples=[MARKER_COLOR_EXAMPLE],
    )


PlaceCategoriesListResponseSchema = make_paginated_response_schema(
    item_type=PlaceCategorySchema,
    description="Response schema for a paginated list of place categories.",
    serialization_alias="categories",
)

# class PlaceCategoriesListResponseSchema(BaseModel):
#     categories: list[PlaceCategorySchema] = Field(
#         ...,
#         description="A list of chat previews that match the specified filters and pagination parameters.",
#     )
#     pagination: OffsetPaginationSchema = Field(
#         ...,
#         description="Pagination information for the retrieved list of place categories.",
#     )
