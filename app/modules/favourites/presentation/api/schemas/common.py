from datetime import datetime

from fastapi import Path
from pydantic import (
    BaseModel,
    Field,
)

from app.modules.favourites.shared.enums import (
    FavouriteEntityPathEnum,
    FavouriteEntityTypeEnum,
)
from app.modules.places.presentation.api.schemas.places.card import PlaceCardSchema
from app.modules.users.presentation.api.schemas.common import USER_ID_EXAMPLE

ENTITY_ID_EXAMPLE = (
    "019caaaa-0000-7000-a000-000000000004"  # TODO: Move to shared core constants
)
ENTITY_TYPE_EXAMPLE = FavouriteEntityTypeEnum.PLACE
ENTITY_TYPE_PATH_EXAMPLE = FavouriteEntityPathEnum.PLACES
ENTITY_CREATED_AT_EXAMPLE = "2026-03-09T04:30:00Z"

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

FavouriteEntityPreview = (
    PlaceCardSchema  # TODO: Add more preview schemas and make it a union of them
)


class FavouriteEntityInfoSchema(BaseModel):
    type: FavouriteEntityTypeEnum = Field(
        ...,
        description="Type of the entity which is added to favourites.",
        examples=[ENTITY_TYPE_EXAMPLE],
    )
    preview: FavouriteEntityPreview = Field(
        ...,
        description="Preview of the entity which is added to favourites. Now it can be only place card preview.",
    )


class FavouriteItemInfoSchema(BaseModel):
    entity: FavouriteEntityInfoSchema = Field(
        ...,
        description="Info about entity which is added to favourites.",
    )
    created_at: datetime = Field(
        ...,
        description="Date and time when the entity was added to favourites.",
        examples=[ENTITY_CREATED_AT_EXAMPLE],
    )
