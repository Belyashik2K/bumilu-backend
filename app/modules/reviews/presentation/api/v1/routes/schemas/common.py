from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.reviews.shared.enums import ReviewEntityTypeEnum

REVIEW_ID_EXAMPLE = "019c95e5-f659-7698-a7dd-7738003a7d23"
ENTITY_ID_EXAMPLE = "019c95e5-f659-7698-a7dd-7738003a7d23"
ENTITY_TYPE_EXAMPLE = ReviewEntityTypeEnum.PLACE
AUTHOR_ID_EXAMPLE = "019c95e5-f659-7698-a7dd-7738003a7d23"
REVIEW_TEXT_EXAMPLE = "idk how to describe this place, but... sorry, i have no time."
REVIEW_RATING_EXAMPLE = 5


class ReviewInfoSchema(BaseModel):
    review_id: UUID7 = Field(
        ..., description="ID of the review", examples=[REVIEW_ID_EXAMPLE]
    )
    entity_id: UUID7 = Field(
        ...,
        description="ID of the entity the review is for",
        examples=[ENTITY_ID_EXAMPLE],
    )
    entity_type: ReviewEntityTypeEnum = Field(
        ...,
        description="Type of the entity the review is for",
        examples=[ENTITY_TYPE_EXAMPLE],
    )
    author_id: UUID7 = Field(
        ..., description="ID of the review's author", examples=[AUTHOR_ID_EXAMPLE]
    )
    text: str | None = Field(
        default=None, description="Text of the review", examples=[REVIEW_TEXT_EXAMPLE]
    )
    rating: int = Field(
        ..., description="Rating given in the review", examples=[REVIEW_RATING_EXAMPLE]
    )
