from pydantic import (
    BaseModel,
)

from app.modules.reviews.presentation.api.schemas.common import (
    RATING_FIELD,
    TEXT_FIELD,
    ReviewInfoSchema,
)


class CreateReviewRequestSchema(BaseModel):
    text: str | None = TEXT_FIELD
    rating: int = RATING_FIELD


class CreateReviewResponseSchema(ReviewInfoSchema): ...
