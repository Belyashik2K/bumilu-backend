from pydantic import (
    BaseModel,
    Field,
)


class PlaceRatingSchema(BaseModel):
    average: float | None = Field(
        None,
        description="Average rating of the place. Can be null if there are no reviews.",
        examples=[5.0],
    )
    reviews_count: int = Field(
        0, description="Number of reviews for the place.", examples=[1984]
    )
