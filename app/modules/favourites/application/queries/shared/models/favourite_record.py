from dataclasses import dataclass
from datetime import datetime

from app.modules.favourites.application.queries.shared.models.favourite_entity import (
    FavouriteEntityReadModel,
    RawFavouriteEntityReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class RawFavouriteRecordReadModel:
    entity: RawFavouriteEntityReadModel
    created_at: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class FavouriteRecordReadModel:
    entity: FavouriteEntityReadModel
    created_at: datetime
