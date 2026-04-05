from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.enums import LanguageEnum

UUID_EXAMPLE = "123e4567-e89b-12d3-a456-426614174000"
LANGUAGE_CODE_EXAMPLE = "ru"
NAME_EXAMPLE = "Чё то для умных людей"
SLUG_EXAMPLE = "museum"
ICON_KEY_EXAMPLE = "landmark"
MARKER_COLOR_EXAMPLE = "#FF0000"


class NewPlaceCategoryTranslationSchema(BaseModel):
    language_code: LanguageEnum = Field(
        ...,
        description="Language code for the translation",
        examples=[LANGUAGE_CODE_EXAMPLE],
    )
    name: str = Field(
        ...,
        description="Translated name of the place category",
        examples=[NAME_EXAMPLE],
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
    translations: list[NewPlaceCategoryTranslationSchema] = Field(
        ...,
        description="List of translations for the place category",
    )


class CreatePlaceCategoryResponseSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="ID of the created place category",
        examples=[UUID_EXAMPLE],
    )
