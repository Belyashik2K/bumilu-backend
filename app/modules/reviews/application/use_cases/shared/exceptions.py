from app.core.shared.domain.value_objects.id import (
    IdVO,
    ReviewIdVO,
)
from app.core.shared.exceptions.application.base import (
    ApplicationForbiddenException,
    ApplicationNotFoundException,
)
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class ReviewNotFound(ApplicationNotFoundException):
    def __init__(self, review_id: ReviewIdVO) -> None:
        super().__init__(message=f"Review with id {review_id} not found")


class ReviewOwnershipViolation(ApplicationForbiddenException):
    def __init__(self) -> None:
        super().__init__(
            message="You do not have permission to perform this action on this review"
        )


class EntityNotFound(ApplicationNotFoundException):
    def __init__(self, entity_type: ReviewEntityTypeEnum, entity_id: IdVO) -> None:
        super().__init__(message=f"{entity_type} with id {entity_id} not found")
