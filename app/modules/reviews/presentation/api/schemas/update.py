from pydantic import (
    BaseModel,
    Field,
)

from app.modules.reviews.presentation.api.schemas.common import (
    REVIEW_RATING_EXAMPLE,
    REVIEW_TEXT_EXAMPLE,
    BaseReviewInfoSchema,
)


class UpdateReviewRequestSchema(BaseModel):
    text: str | None = Field(
        None,
        description="Text of the review",
        examples=[REVIEW_TEXT_EXAMPLE],
        min_length=10,
        max_length=1000,
    )
    rating: int | None = Field(
        None,
        description="Rating given in the review",
        examples=[REVIEW_RATING_EXAMPLE],
        ge=1,
        le=5,
    )


class UpdateReviewResponseSchema(BaseReviewInfoSchema): ...
