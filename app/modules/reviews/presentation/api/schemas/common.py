from typing import Annotated

from fastapi import (
    Depends,
    Path,
    Query,
)
from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.reviews.shared.enums import (
    ReviewEntityPathEnum,
    ReviewEntityTypeEnum,
)
from app.modules.users.presentation.api.schemas.common import USER_ID_EXAMPLE

REVIEW_ID_EXAMPLE = "019caaaa-0000-7000-a000-000000000003"
ENTITY_ID_EXAMPLE = (
    "019caaaa-0000-7000-a000-000000000004"  # TODO: Move to shared core constants
)
ENTITY_TYPE_EXAMPLE = ReviewEntityTypeEnum.PLACE
ENTITY_TYPE_PATH_EXAMPLE = ReviewEntityPathEnum.PLACES
AUTHOR_ID_EXAMPLE = USER_ID_EXAMPLE
REVIEW_TEXT_EXAMPLE = "idk how to describe this place, but... sorry, i have no time."
REVIEW_RATING_EXAMPLE = 5

TEXT_FIELD = Field(
    ...,
    description="Text of the review",
    examples=[REVIEW_TEXT_EXAMPLE],
    min_length=10,
    max_length=1000,
)
RATING_FIELD = Field(
    ...,
    description="Rating given in the review",
    examples=[REVIEW_RATING_EXAMPLE],
    ge=1,
    le=5,
)

REVIEW_ID_PATH = Path(
    ...,
    description="ID of the review",
    example=REVIEW_ID_EXAMPLE,
)
ENTITY_TYPE_PATH = Path(
    ...,
    description="Type of the entity the review is for",
    example=ENTITY_TYPE_PATH_EXAMPLE,
)
ENTITY_ID_PATH = Path(
    ...,
    description="ID of the entity the review is for",
    example=ENTITY_ID_EXAMPLE,
)
USER_ID_PATH = Path(
    ...,
    description="ID of the user (author) for which reviews are fetched",
    example=AUTHOR_ID_EXAMPLE,
)


class ReviewAuthorInfoSchema(BaseModel):
    id: UUID7 = Field(
        ..., description="Review author's ID", examples=[AUTHOR_ID_EXAMPLE]
    )


class ReviewEntityInfoSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="ID of the entity the review is for",
        examples=[ENTITY_ID_EXAMPLE],
    )
    type: ReviewEntityTypeEnum = Field(
        ...,
        description="Type of the entity the review is for",
        examples=[ENTITY_TYPE_EXAMPLE],
    )


class BaseReviewInfoSchema(BaseModel):
    review_id: UUID7 = Field(
        ..., description="ID of the review", examples=[REVIEW_ID_EXAMPLE]
    )
    text: str | None = TEXT_FIELD
    rating: int = RATING_FIELD


class ReviewInfoSchema(BaseReviewInfoSchema):
    entity: ReviewEntityInfoSchema = Field(
        ..., description="Information about the entity the review is for"
    )
    author: ReviewAuthorInfoSchema = Field(
        ..., description="Information about the author of the review"
    )


class ReviewsFilters(BaseModel):
    entity_type: ReviewEntityTypeEnum | None = Field(
        None,
        description="Filter reviews by their entity type.",
        examples=[ENTITY_TYPE_EXAMPLE],
    )


def get_reviews_filters(
    entity_type: Annotated[
        ReviewEntityTypeEnum | None,
        Query(
            description="Filter reviews items by their entity type. If not provided, review items of all entity types will be returned.",
            examples=[ENTITY_TYPE_EXAMPLE],
        ),
    ] = None,
) -> ReviewsFilters:
    return ReviewsFilters(entity_type=entity_type)


ReviewsFiltersDep = Annotated[ReviewsFilters, Depends(get_reviews_filters)]
