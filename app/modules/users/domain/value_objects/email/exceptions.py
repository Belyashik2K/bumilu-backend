from app.core.shared.exceptions.domain.base import DomainValidationException


class InvalidEmailFormat(DomainValidationException):
    def __init__(self) -> None:
        super().__init__("Invalid email format")


class EmailTldNotAllowed(DomainValidationException):
    def __init__(self, tld: str) -> None:
        super().__init__("Email TLD is not allowed", details={"tld": tld})


class EmailDomainNotAllowed(DomainValidationException):
    def __init__(self, domain: str) -> None:
        super().__init__("Email domain is not allowed", details={"domain": domain})
