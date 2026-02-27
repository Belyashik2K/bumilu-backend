#
# class GetAllReviewsForEntityOutputDTO:
#     entity_id: UUID
#     items: list[ReviewInfoDTO] = field(default_factory=list)
from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.reviews.presentation.api.schemas.common import (
    ENTITY_ID_EXAMPLE,
    ReviewInfoSchema,
)
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class ReducedReviewInfoSchema(ReviewInfoSchema):
    entity_id: UUID7 = Field(exclude=True)
    entity_type: ReviewEntityTypeEnum = Field(exclude=True)


class GetAllReviewsForEntityResponseSchema(BaseModel):
    entity_id: UUID7 = Field(
        ...,
        description="ID of the entity for which reviews are fetched",
        examples=[ENTITY_ID_EXAMPLE],
    )
    entity_type: ReviewEntityTypeEnum = Field(
        ...,
        description="Type of the entity for which reviews are fetched",
    )
    items: list[ReducedReviewInfoSchema] = Field(
        ..., description="List of reviews for the entity fetched"
    )
