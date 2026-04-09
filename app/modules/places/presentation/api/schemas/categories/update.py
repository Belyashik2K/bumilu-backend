from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.categories.create import (
    ICON_KEY_EXAMPLE,
    MARKER_COLOR_EXAMPLE,
    NAME_EXAMPLE,
    SLUG_EXAMPLE,
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


class UpdatePlaceCategoryTranslationRequestSchema(BaseModel):
    name: str | None = Field(
        ...,
        description="New name for the place category in the specified language",
        examples=[NAME_EXAMPLE],
    )
