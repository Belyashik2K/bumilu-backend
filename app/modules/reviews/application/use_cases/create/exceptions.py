from app.core.shared.exceptions.application.base import ApplicationConflictException
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class ReviewAlreadyExists(ApplicationConflictException):
    def __init__(self, entity_type: ReviewEntityTypeEnum) -> None:
        super().__init__(
            message=f"You have already created a review for this {entity_type}"
        )
