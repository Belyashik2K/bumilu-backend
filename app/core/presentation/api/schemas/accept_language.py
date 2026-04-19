from typing import Annotated

from fastapi import (
    Depends,
    Header,
)
from pydantic import BaseModel

from app.core.enums import LanguageEnum


class AcceptLanguageQuery(BaseModel):
    language: LanguageEnum


def get_accept_language(
    accept_language: Annotated[
        LanguageEnum,
        Header(
            alias="Accept-Language",
            description="Requested language for the response.",
        ),
    ],
) -> AcceptLanguageQuery:
    return AcceptLanguageQuery(language=accept_language)


AcceptLanguageDep = Annotated[AcceptLanguageQuery, Depends(get_accept_language)]
