from abc import (
    ABC,
    abstractmethod,
)

from app.core.domain.value_objects.id import PrincipalIdVO
from app.modules.favourites.domain.models.favourite import Favourite


class IFavouriteRepository(ABC):
    @abstractmethod
    async def add_if_not_exists(
        self,
        favourite: Favourite,
    ) -> None: ...

    @abstractmethod
    async def remove_if_exists(
        self,
        favourite: Favourite,
    ) -> None: ...

    @abstractmethod
    async def get_all_by_user_id(
        self,
        user_id: PrincipalIdVO,
    ) -> list[Favourite]: ...
