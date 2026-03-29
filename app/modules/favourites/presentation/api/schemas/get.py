from typing import Annotated

from fastapi import (
    Depends,
    Query,
)
from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import OffsetPaginationSchema
from app.modules.favourites.presentation.api.schemas.common import (
    ENTITY_TYPE_EXAMPLE,
    FavouriteItemInfoSchema,
)
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum
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


class FavouritesFilters(BaseModel):
    entity_type: FavouriteEntityTypeEnum | None = Field(
        None,
        description="Filter favourite items by their entity type.",
        examples=[ENTITY_TYPE_EXAMPLE],
    )


def get_favourites_filters(
    entity_type: Annotated[
        FavouriteEntityTypeEnum | None,
        Query(
            description="Filter favourite items by their entity type. If not provided, favourite items of all entity types will be returned.",
            examples=[ENTITY_TYPE_EXAMPLE],
        ),
    ] = None,
) -> FavouritesFilters:
    return FavouritesFilters(entity_type=entity_type)


FavouritesFiltersDep = Annotated[FavouritesFilters, Depends(get_favourites_filters)]
