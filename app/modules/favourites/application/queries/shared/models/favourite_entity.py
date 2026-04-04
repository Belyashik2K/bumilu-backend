from dataclasses import dataclass
from uuid import UUID

from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum
from app.modules.places.application.queries.places.shared.views import PlaceCardView


@dataclass(frozen=True, slots=True, kw_only=True)
class RawFavouriteEntityReadModel:
    id: UUID
    type: FavouriteEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class FavouritePlaceEntityReadModel(RawFavouriteEntityReadModel):
    preview: PlaceCardView


FavouriteEntityReadModel = FavouritePlaceEntityReadModel

# TODO: Add route favourite entity read model when route favourites are implemented
