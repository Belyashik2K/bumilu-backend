import re
from dataclasses import dataclass
from re import Pattern
from typing import (
    ClassVar,
)

from app.core.domain.value_objects.string.exceptions import InvalidString


@dataclass(frozen=True, slots=True)
class BaseStringVO:
    value: str | None

    min_length: ClassVar[int | None] = None
    max_length: ClassVar[int | None] = None
    pattern: ClassVar[str | Pattern[str] | None] = None
    forbidden_pattern: ClassVar[str | Pattern[str] | None] = None
    strip_value: ClassVar[bool] = True
    to_lower: ClassVar[bool] = False
    to_upper: ClassVar[bool] = False
    nullable: ClassVar[bool] = False

    def __post_init__(self) -> None:
        value = self.value

        if value is None:
            if self.nullable:
                return
            raise InvalidString(f"{self.__class__.__name__}: value cannot be None")

        if not isinstance(value, str):
            raise InvalidString(
                f"{self.__class__.__name__}: value must be str, got {type(value).__name__}"
            )

        if self.to_lower and self.to_upper:
            raise InvalidString(
                f"{self.__class__.__name__}: only one of to_lower or to_upper can be enabled"
            )

        if self.strip_value:
            value = value.strip()

        if self.to_lower:
            value = value.lower()
        elif self.to_upper:
            value = value.upper()

        self._validate(value)
        value = self.additional_validate(value)

        if value != self.value:
            object.__setattr__(self, "value", value)

    @classmethod
    def _validate(cls, value: str) -> None:
        cls._validate_length(value)
        cls._validate_pattern(value)
        cls._validate_forbidden_pattern(value)

    @classmethod
    def _validate_length(cls, value: str) -> None:
        if cls.min_length is not None and len(value) < cls.min_length:
            raise InvalidString(
                f"{cls.__name__}: length must be >= {cls.min_length}, got {len(value)}"
            )

        if cls.max_length is not None and len(value) > cls.max_length:
            raise InvalidString(
                f"{cls.__name__}: length must be <= {cls.max_length}, got {len(value)}"
            )

    @classmethod
    def _validate_pattern(cls, value: str) -> None:
        if cls.pattern is None:
            return

        regex = cls._compile_pattern(cls.pattern)
        if regex.fullmatch(value) is None:
            raise InvalidString(
                f"{cls.__name__}: value does not match pattern: {value!r}"
            )

    @classmethod
    def _validate_forbidden_pattern(cls, value: str) -> None:
        if cls.forbidden_pattern is None:
            return

        regex = cls._compile_pattern(cls.forbidden_pattern)
        if regex.search(value) is not None:
            raise InvalidString(
                f"{cls.__name__}: value contains forbidden characters: {value!r}"
            )

    @staticmethod
    def _compile_pattern(pattern: str | Pattern[str]) -> Pattern[str]:
        return re.compile(pattern) if isinstance(pattern, str) else pattern

    @classmethod
    def additional_validate(cls, value: str) -> str:
        return value

    def __str__(self) -> str:
        return "" if self.value is None else self.value
