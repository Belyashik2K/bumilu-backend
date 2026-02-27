from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.reviews.presentation.api.v1.routes.schemas.common import (
    ENTITY_ID_EXAMPLE,
    RATING_FIELD,
    TEXT_FIELD,
    ReviewInfoSchema,
)


class CreateReviewRequestSchema(BaseModel):
    entity_id: UUID7 = Field(
        ...,
        description="ID of the entity the review is for",
        examples=[ENTITY_ID_EXAMPLE],
    )
    text: str | None = TEXT_FIELD
    rating: int = RATING_FIELD


class CreateReviewResponseSchema(ReviewInfoSchema): ...
