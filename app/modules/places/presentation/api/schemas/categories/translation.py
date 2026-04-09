from pydantic import (
    BaseModel,
    Field,
)

from app.core.enums import LanguageEnum
from app.modules.places.presentation.api.schemas.categories.examples import (
    LANGUAGE_CODE_EXAMPLE,
    NAME_EXAMPLE,
)


class PlaceCategoryTranslationSchema(BaseModel):
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


class UpdatePlaceCategoryTranslationRequestSchema(BaseModel):
    name: str | None = Field(
        ...,
        description="New name for the place category in the specified language",
        examples=[NAME_EXAMPLE],
    )
