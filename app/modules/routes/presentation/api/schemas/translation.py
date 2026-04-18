from pydantic import (
    BaseModel,
    Field,
)

from app.core.enums import LanguageEnum
from app.modules.routes.presentation.api.schemas.examples import (
    DESCRIPTION_EXAMPLE,
    LANGUAGE_CODE_EXAMPLE,
    SHORT_DESCRIPTION_EXAMPLE,
    TITLE_EXAMPLE,
)


class BaseRouteTranslationSchema(BaseModel):
    language_code: LanguageEnum = Field(
        ...,
        description="Language code for the translation",
        examples=[LANGUAGE_CODE_EXAMPLE],
    )
    title: str = Field(
        ...,
        description="Title of the route in the specified language",
        examples=[TITLE_EXAMPLE],
    )
    description: str = Field(
        ...,
        description="Description of the route in the specified language",
        examples=[DESCRIPTION_EXAMPLE],
    )
    short_description: str = Field(
        ...,
        description="Short description of the route in the specified language",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )


class CreateRouteTranslationRequestSchema(BaseRouteTranslationSchema): ...


class UpdateRouteTranslationRequestSchema(BaseModel):
    title: str | None = Field(
        None,
        description="Title of the route in the specified language",
        examples=[TITLE_EXAMPLE],
    )
    description: str | None = Field(
        None,
        description="Description of the route in the specified language",
        examples=[DESCRIPTION_EXAMPLE],
    )
    short_description: str | None = Field(
        None,
        description="Short description of the route in the specified language",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
