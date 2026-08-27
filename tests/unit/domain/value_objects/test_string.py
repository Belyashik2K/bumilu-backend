from dataclasses import dataclass
from typing import ClassVar

import pytest
from app.core.domain.value_objects.string.exceptions import InvalidString
from app.core.domain.value_objects.string.object import BaseStringVO


@dataclass(frozen=True, slots=True)
class _LengthConstrainedVO(BaseStringVO):
    min_length: ClassVar[int | None] = 2
    max_length: ClassVar[int | None] = 5


@dataclass(frozen=True, slots=True)
class _PatternVO(BaseStringVO):
    pattern: ClassVar[str | None] = r"^[a-z]+$"


@dataclass(frozen=True, slots=True)
class _ForbiddenPatternVO(BaseStringVO):
    forbidden_pattern: ClassVar[str | None] = r"<script>"


@dataclass(frozen=True, slots=True)
class _NullableVO(BaseStringVO):
    nullable: ClassVar[bool] = True
    min_length: ClassVar[int | None] = 2


@dataclass(frozen=True, slots=True)
class _LowercaseVO(BaseStringVO):
    to_lower: ClassVar[bool] = True


@dataclass(frozen=True, slots=True)
class _UppercaseVO(BaseStringVO):
    to_upper: ClassVar[bool] = True


@dataclass(frozen=True, slots=True)
class _ConflictingCaseVO(BaseStringVO):
    to_lower: ClassVar[bool] = True
    to_upper: ClassVar[bool] = True


@dataclass(frozen=True, slots=True)
class _NoStripVO(BaseStringVO):
    strip_value: ClassVar[bool] = False


class TestBaseStringVODefaults:
    def test_accepts_any_non_empty_string(self) -> None:
        vo = BaseStringVO("hello")

        assert vo.value == "hello"

    def test_raises_when_none_and_not_nullable(self) -> None:
        with pytest.raises(InvalidString):
            BaseStringVO(None)

    def test_raises_when_value_is_not_a_string(self) -> None:
        with pytest.raises(InvalidString):
            BaseStringVO(123)  # type: ignore[arg-type]

    def test_strips_surrounding_whitespace_by_default(self) -> None:
        vo = BaseStringVO("  hello  ")

        assert vo.value == "hello"

    def test_str_returns_value(self) -> None:
        vo = BaseStringVO("hello")

        assert str(vo) == "hello"

    def test_str_returns_empty_string_for_none_value(self) -> None:
        vo = _NullableVO(None)

        assert str(vo) == ""


class TestBaseStringVOLength:
    def test_accepts_value_within_bounds(self) -> None:
        vo = _LengthConstrainedVO("abc")

        assert vo.value == "abc"

    @pytest.mark.parametrize("value", ["ab", "abcde"])
    def test_accepts_boundary_lengths(self, value: str) -> None:
        vo = _LengthConstrainedVO(value)

        assert vo.value == value

    def test_raises_when_below_min_length(self) -> None:
        with pytest.raises(InvalidString):
            _LengthConstrainedVO("a")

    def test_raises_when_above_max_length(self) -> None:
        with pytest.raises(InvalidString):
            _LengthConstrainedVO("abcdef")


class TestBaseStringVOPattern:
    def test_accepts_value_matching_pattern(self) -> None:
        vo = _PatternVO("hello")

        assert vo.value == "hello"

    def test_raises_when_value_does_not_match_pattern(self) -> None:
        with pytest.raises(InvalidString):
            _PatternVO("Hello123")


class TestBaseStringVOForbiddenPattern:
    def test_accepts_value_without_forbidden_pattern(self) -> None:
        vo = _ForbiddenPatternVO("hello world")

        assert vo.value == "hello world"

    def test_raises_when_forbidden_pattern_present(self) -> None:
        with pytest.raises(InvalidString):
            _ForbiddenPatternVO("hello <script>alert(1)</script>")


class TestBaseStringVONullable:
    def test_accepts_none_when_nullable(self) -> None:
        vo = _NullableVO(None)

        assert vo.value is None

    def test_still_validates_non_none_value(self) -> None:
        with pytest.raises(InvalidString):
            _NullableVO("a")


class TestBaseStringVOCaseTransform:
    def test_lowercases_value_when_enabled(self) -> None:
        vo = _LowercaseVO("HELLO")

        assert vo.value == "hello"

    def test_uppercases_value_when_enabled(self) -> None:
        vo = _UppercaseVO("hello")

        assert vo.value == "HELLO"

    def test_raises_when_both_lower_and_upper_enabled(self) -> None:
        with pytest.raises(InvalidString):
            _ConflictingCaseVO("hello")


class TestBaseStringVOStripBehavior:
    def test_preserves_whitespace_when_strip_disabled(self) -> None:
        vo = _NoStripVO("  hello  ")

        assert vo.value == "  hello  "
