from dataclasses import dataclass

from app.core.enums import LanguageEnum


@dataclass(frozen=True, kw_only=True)
class LanguageMixin:
    language: LanguageEnum
