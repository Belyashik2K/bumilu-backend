from app.core.exceptions.domain.base import DomainValidationException


class InvalidSlug(DomainValidationException):
    def __init__(self, slug: str) -> None:
        super().__init__(
            message=f"Invalid slug: {slug}. Slug must be lowercase, contain only english letters.",
            details={"slug": slug},
        )
