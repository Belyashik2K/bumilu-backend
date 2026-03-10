from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.reviews.presentation.api.schemas.common import (
    RATING_FIELD,
    REVIEW_ID_EXAMPLE,
    TEXT_FIELD,
)


class CreateReviewRequestSchema(BaseModel):
    text: str | None = TEXT_FIELD
    rating: int = RATING_FIELD


class CreateReviewResponseSchema(BaseModel):
    review_id: UUID7 = Field(
        ..., description="ID of the created review", examples=[REVIEW_ID_EXAMPLE]
    )
