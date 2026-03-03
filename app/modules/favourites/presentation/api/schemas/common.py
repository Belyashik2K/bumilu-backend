from fastapi import Path
from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.favourites.shared.enums.favourite_entity import (
    FavouriteEntityPathEnum,
    FavouriteEntityTypeEnum,
)
from app.modules.reviews.presentation.api.schemas.common import (
    ENTITY_ID_EXAMPLE,
)
from app.modules.users.presentation.api.schemas.common import USER_ID_EXAMPLE

ENTITY_TYPE_EXAMPLE = FavouriteEntityTypeEnum.PLACE
ENTITY_TYPE_PATH_EXAMPLE = FavouriteEntityPathEnum.PLACES

ENTITY_TYPE_PATH = Path(
    ...,
    description="Type of the entity which you want to add to favourites.",
    example=ENTITY_TYPE_PATH_EXAMPLE,
)
ENTITY_ID_PATH = Path(
    ...,
    description="ID of the entity which you want to add to favourites",
    example=ENTITY_ID_EXAMPLE,
)
USER_ID_PATH = Path(
    ...,
    description="ID of the user for which you want to get favourites.",
    example=USER_ID_EXAMPLE,
)


class FavouriteItemInfoSchema(BaseModel):
    entity_type: FavouriteEntityTypeEnum = Field(
        ...,
        description="Type of the entity which is added to favourites.",
        examples=[ENTITY_TYPE_EXAMPLE],
    )
    entity_id: UUID7 = Field(
        ...,
        description="ID of the entity which is added to favourites.",
        examples=[ENTITY_ID_EXAMPLE],
    )
