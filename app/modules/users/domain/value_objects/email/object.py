import re
from dataclasses import dataclass

from app.modules.users.domain.value_objects.email.exceptions import (
    EmailDomainNotAllowed,
    EmailTldNotAllowed,
    InvalidEmailFormat,
)

_BASIC_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,63}$")

_BLOCKED_TLDS = {"lu"}  # ну а чё они 100 баксов стоят, bumi.lu явно не пропустим
_BLOCKED_DOMAINS = {"bumi.lu"}  # вот когда сами купим, тогда и пропустим


@dataclass(frozen=True, slots=True)
class EmailVO:
    value: str

    @staticmethod
    def _validate_tld(tld: str) -> None:
        if tld in _BLOCKED_TLDS:
            raise EmailTldNotAllowed(tld)

    @staticmethod
    def _validate_domain(domain: str) -> None:
        if domain in _BLOCKED_DOMAINS:
            raise EmailDomainNotAllowed(domain)

    @staticmethod
    def _validate_email_format(email: str) -> None:
        if not _BASIC_EMAIL_RE.match(email):
            raise InvalidEmailFormat()

    @classmethod
    def from_string(cls, email: str) -> "EmailVO":
        return cls(email)

    def __post_init__(self):
        email = self.value.strip().lower()

        self._validate_email_format(email)

        _, domain = email.rsplit("@", 1)
        tld = domain.rsplit(".", 1)[-1]

        self._validate_tld(tld)
        self._validate_domain(domain)

        object.__setattr__(self, "value", email)

    def __str__(self) -> str:
        return self.value
