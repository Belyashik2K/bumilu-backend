from pydantic import (
    BaseModel,
    Field,
)

from app.modules.favourites.presentation.api.schemas.common import (
    FavouriteItemInfoSchema,
)


class GetAllFavouritesByUserResponseSchema(BaseModel):
    items: list[FavouriteItemInfoSchema] = Field(
        ...,
        description="List of favourite items for the user.",
    )
