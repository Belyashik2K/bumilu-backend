from enum import StrEnum
from typing import Self


class LanguageEnum(StrEnum):
    ZH = "zh"
    EN = "en"
    RU = "ru"

    @classmethod
    def default(cls) -> Self:
        return cls.EN
