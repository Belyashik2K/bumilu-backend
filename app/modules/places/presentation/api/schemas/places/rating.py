from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.examples import (
    AVERAGE_EXAMPLE,
    REVIEWS_COUNT_EXAMPLE,
)


class PlaceRatingSchema(BaseModel):
    average: float | None = Field(
        None,
        description="Average rating of the place. Can be null if there are no reviews.",
        examples=[AVERAGE_EXAMPLE],
    )
    reviews_count: int = Field(
        0,
        description="Number of reviews for the place.",
        examples=[REVIEWS_COUNT_EXAMPLE],
    )
