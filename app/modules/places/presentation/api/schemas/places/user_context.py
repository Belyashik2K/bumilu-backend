from pydantic import (
    BaseModel,
    Field,
)


class PlaceUserContextSchema(BaseModel):
    is_favorite: bool = Field(
        ...,
        description="Whether the place is in the user's favorites",
        examples=[True],
    )
