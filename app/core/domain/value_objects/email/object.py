import re
from dataclasses import (
    dataclass,
)
from typing import (
    ClassVar,
    Self,
)

from app.core.domain.value_objects.email.exceptions import (
    EmailDomainNotAllowed,
    EmailTldNotAllowed,
    InvalidEmailFormat,
)

_BASIC_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,63}$")


@dataclass(frozen=True, slots=True)
class BaseEmailVO:
    value: str

    ALLOWED_TLDS: ClassVar[set[str] | None] = None
    BLOCKED_TLDS: ClassVar[set[str]] = set()

    ALLOWED_DOMAINS: ClassVar[set[str] | None] = None
    BLOCKED_DOMAINS: ClassVar[set[str]] = set()

    @classmethod
    def _validate_tld(cls, tld: str) -> None:
        if cls.ALLOWED_TLDS is not None and tld not in cls.ALLOWED_TLDS:
            raise EmailTldNotAllowed(tld)

        if tld in cls.BLOCKED_TLDS:
            raise EmailTldNotAllowed(tld)

    @classmethod
    def _validate_domain(cls, domain: str) -> None:
        if cls.ALLOWED_DOMAINS is not None and domain not in cls.ALLOWED_DOMAINS:
            raise EmailDomainNotAllowed(domain)

        if domain in cls.BLOCKED_DOMAINS:
            raise EmailDomainNotAllowed(domain)

    @staticmethod
    def _validate_email_format(email: str) -> None:
        if not _BASIC_EMAIL_RE.match(email):
            raise InvalidEmailFormat()

    @classmethod
    def from_string(cls, email: str) -> Self:
        return cls(email)

    @property
    def fingerprint(self) -> str:
        email_id_part, domain_part = self.value.split("@", 1)
        n = len(email_id_part)

        if n <= 2:
            masked = email_id_part[0] + "*" * (n - 1)
        else:
            masked = email_id_part[0] + "*" * (n - 2) + email_id_part[-1]

        return masked + "@" + domain_part

    def __post_init__(self) -> None:
        email = self.value.strip().lower()

        self._validate_email_format(email)

        _, domain = email.rsplit("@", 1)
        tld = domain.rsplit(".", 1)[-1]

        type(self)._validate_tld(tld)
        type(self)._validate_domain(domain)

        object.__setattr__(self, "value", email)

    def __str__(self) -> str:
        return self.value
