from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from app.core.shared.domain.value_objects.id import (
    IdVO,
    UserIdVO,
)
from app.core.shared.utils import get_current_dt
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class Favourite:
    user_id: UserIdVO
    entity_type: FavouriteEntityTypeEnum
    entity_id: IdVO
    created_at: datetime = field(default_factory=get_current_dt)

    @classmethod
    def create(
        cls,
        user_id: UserIdVO,
        entity_type: FavouriteEntityTypeEnum,
        entity_id: IdVO,
    ) -> "Favourite":
        return cls(
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
        )
