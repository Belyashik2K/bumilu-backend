from pydantic import (
    BaseModel,
    Field,
)

from app.core.enums import LanguageEnum
from app.core.presentation.api.schemas.pagination import make_paginated_response_schema
from app.modules.places.presentation.api.schemas.places.examples import (
    DESCRIPTION_EXAMPLE,
    DISPLAY_ADDRESS_EXAMPLE,
    LANGUAGE_CODE_EXAMPLE,
    SHORT_DESCRIPTION_EXAMPLE,
    TITLE_EXAMPLE,
)


class BasePlaceTranslationSchema(BaseModel):
    language_code: LanguageEnum = Field(
        ...,
        description="Language code for the translation",
        examples=[LANGUAGE_CODE_EXAMPLE],
    )
    title: str = Field(
        ...,
        description="Title of the place in the specified language",
        examples=[TITLE_EXAMPLE],
    )
    description: str = Field(
        ...,
        description="Description of the place in the specified language",
        examples=[DESCRIPTION_EXAMPLE],
    )
    short_description: str = Field(
        ...,
        description="Short description of the place in the specified language",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    display_address: str = Field(
        ...,
        description="Display address of the place in the specified language",
        examples=[DISPLAY_ADDRESS_EXAMPLE],
    )


class CreatePlaceTranslationRequestSchema(BasePlaceTranslationSchema): ...


class UpdatePlaceTranslationRequestSchema(BaseModel):
    title: str | None = Field(
        None,
        description="Title of the place in the specified language",
        examples=[TITLE_EXAMPLE],
    )
    description: str | None = Field(
        None,
        description="Description of the place in the specified language",
        examples=[DESCRIPTION_EXAMPLE],
    )
    short_description: str | None = Field(
        None,
        description="Short description of the place in the specified language",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    display_address: str | None = Field(
        None,
        description="Display address of the place in the specified language",
        examples=[DISPLAY_ADDRESS_EXAMPLE],
    )


PaginatedPlaceTranslationListResponseSchema = make_paginated_response_schema(
    item_type=BasePlaceTranslationSchema,
    description="Paginated response schema for a list of place translations",
)
