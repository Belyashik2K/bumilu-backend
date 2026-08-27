from dataclasses import dataclass
from typing import ClassVar

import pytest
from app.core.domain.value_objects.email.exceptions import (
    EmailDomainNotAllowed,
    EmailTldNotAllowed,
    InvalidEmailFormat,
)
from app.core.domain.value_objects.email.object import BaseEmailVO


@dataclass(frozen=True, slots=True)
class _RestrictedEmailVO(BaseEmailVO):
    ALLOWED_TLDS: ClassVar[set[str] | None] = {"com", "ru"}
    BLOCKED_TLDS: ClassVar[set[str]] = {"xyz"}
    ALLOWED_DOMAINS: ClassVar[set[str] | None] = {"allowed.com"}
    BLOCKED_DOMAINS: ClassVar[set[str]] = {"blocked.com"}


class TestBaseEmailVONormalization:
    def test_strips_and_lowercases_value(self) -> None:
        email = BaseEmailVO.from_string("  User@Example.COM  ")

        assert email.value == "user@example.com"

    def test_str_returns_normalized_value(self) -> None:
        email = BaseEmailVO.from_string("User@Example.com")

        assert str(email) == "user@example.com"


class TestBaseEmailVOFormatValidation:
    @pytest.mark.parametrize(
        "raw",
        [
            "not-an-email",
            "user@",
            "@example.com",
            "user@example",
            "user example@example.com",
            "user@example.c",
        ],
    )
    def test_raises_on_invalid_format(self, raw: str) -> None:
        with pytest.raises(InvalidEmailFormat):
            BaseEmailVO.from_string(raw)

    def test_accepts_well_formed_email(self) -> None:
        email = BaseEmailVO.from_string("user@example.com")

        assert email.value == "user@example.com"


class TestEmailVOTldRestrictions:
    def test_raises_when_tld_not_in_allowed_list(self) -> None:
        with pytest.raises(EmailTldNotAllowed):
            _RestrictedEmailVO.from_string("user@example.org")

    def test_raises_when_tld_is_blocked(self) -> None:
        with pytest.raises(EmailTldNotAllowed):
            _RestrictedEmailVO.from_string("user@allowed.xyz")

    def test_accepts_email_with_allowed_tld_and_domain(self) -> None:
        email = _RestrictedEmailVO.from_string("user@allowed.com")

        assert email.value == "user@allowed.com"


class TestEmailVODomainRestrictions:
    def test_raises_when_domain_not_in_allowed_list(self) -> None:
        with pytest.raises(EmailDomainNotAllowed):
            _RestrictedEmailVO.from_string("user@other.com")

    def test_raises_when_domain_is_blocked(self) -> None:
        with pytest.raises(EmailDomainNotAllowed):
            _RestrictedEmailVO.from_string("user@blocked.com")


class TestEmailVOFingerprint:
    def test_masks_middle_of_local_part(self) -> None:
        email = BaseEmailVO.from_string("abcdef@example.com")

        assert email.fingerprint == "a****f@example.com"

    def test_masks_two_char_local_part(self) -> None:
        email = BaseEmailVO.from_string("ab@example.com")

        assert email.fingerprint == "a*@example.com"

    def test_leaves_single_char_local_part_unmasked(self) -> None:
        email = BaseEmailVO.from_string("a@example.com")

        assert email.fingerprint == "a@example.com"
