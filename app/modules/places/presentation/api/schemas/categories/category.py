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


class PlaceCategoryBaseSchema(BaseModel):
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


class PlaceCategorySchema(PlaceCategoryBaseSchema):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place category",
        examples=[UUID_EXAMPLE],
    )


class LocalizedPlaceCategorySchema(PlaceCategorySchema):
    name: str = Field(
        ...,
        description="The localized name of the place category.",
        examples=[NAME_EXAMPLE],
    )


class CreatePlaceCategoryRequestSchema(PlaceCategoryBaseSchema):
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


class UpdatePlaceCategoryRequestSchema(BaseModel):
    slug: str | None = Field(
        None,
        description="Unique slug for the place category",
        examples=[SLUG_EXAMPLE],
    )
    icon_key: str | None = Field(
        None,
        description="Icon key for frontend from Lucide Icons",
        examples=[ICON_KEY_EXAMPLE],
    )
    marker_color: str | None = Field(
        None,
        description="Hex color code for the marker",
        examples=[MARKER_COLOR_EXAMPLE],
    )


PlaceCategoriesListResponseSchema = make_paginated_response_schema(
    item_type=LocalizedPlaceCategorySchema,
    description="Response schema for a paginated list of place categories.",
    validation_alias="categories",
)
AdminPlaceCategoriesListResponseSchema = make_paginated_response_schema(
    item_type=PlaceCategorySchema,
    description="Response schema for a paginated list of place categories for admin users",
    validation_alias="categories",
)
