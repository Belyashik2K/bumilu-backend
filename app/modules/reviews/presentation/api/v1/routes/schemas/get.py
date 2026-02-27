#
# class GetAllReviewsForEntityOutputDTO:
#     entity_id: UUID
#     items: list[ReviewInfoDTO] = field(default_factory=list)
from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.reviews.presentation.api.v1.routes.schemas.common import (
    ENTITY_ID_EXAMPLE,
    ReviewInfoSchema,
)


class GetAllReviewsForEntityResponseSchema(BaseModel):
    entity_id: UUID7 = Field(
        ...,
        description="ID of the entity for which reviews are fetched",
        examples=[ENTITY_ID_EXAMPLE],
    )
    items: list[ReviewInfoSchema] = Field(
        ..., description="List of reviews for the entity fetched"
    )
