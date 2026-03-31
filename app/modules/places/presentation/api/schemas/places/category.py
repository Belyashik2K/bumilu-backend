from pydantic import (
    BaseModel,
    Field,
)

NAME_EXAMPLE = "What they don't talk about in polite society"


class PlaceCardCategorySchema(BaseModel):
    name: str = Field(
        ...,
        description="The name of the category.",
        examples=[NAME_EXAMPLE],
    )
