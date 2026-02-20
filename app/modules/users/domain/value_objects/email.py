import re
from dataclasses import dataclass

_BASIC_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,63}$")

_BLOCKED_TLDS = {"lu"}  # ну а чё они 100 баксов стоят, bumi.lu явно не пропустим
_BLOCKED_DOMAINS = set("bumi.lu")  # вот когда сами купим, тогда и пропустим


@dataclass(frozen=True, slots=True)
class EmailVO:
    value: str

    @staticmethod
    def _validate_tld(tld: str) -> None:
        if tld in _BLOCKED_TLDS:
            raise ValueError(f"Email TLD '.{tld}' is not allowed")

    @staticmethod
    def _validate_domain(domain: str) -> None:
        if domain in _BLOCKED_DOMAINS:
            raise ValueError("Email domain is not allowed")

    @staticmethod
    def _validate_email_format(email: str) -> None:
        if not _BASIC_EMAIL_RE.match(email):
            raise ValueError("Invalid email format")

    def __post_init__(self):
        email = self.value.strip().lower()

        self._validate_email_format(email)

        local, domain = email.rsplit("@", 1)
        tld = domain.rsplit(".", 1)[-1]

        self._validate_tld(tld)
        self._validate_domain(domain)

        object.__setattr__(self, "value", email)

    def __str__(self) -> str:
        return self.value
