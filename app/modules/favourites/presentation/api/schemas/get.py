from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.shared.presentation.schemas.pagination import OffsetPaginationSchema
from app.modules.favourites.presentation.api.schemas.common import (
    FavouriteItemInfoSchema,
)
from app.modules.users.presentation.api.schemas.common import USER_ID_EXAMPLE


class GetAllFavouritesByUserResponseSchema(BaseModel):
    user_id: UUID7 = Field(
        ...,
        description="The unique identifier of the user whose favourite items are being retrieved.",
        examples=[USER_ID_EXAMPLE],
    )
    favourites: list[FavouriteItemInfoSchema] = Field(
        ...,
        description="List of favourite items for the user.",
    )
    pagination: OffsetPaginationSchema = Field(
        ...,
        description="Pagination information for the list of favourite items.",
    )
