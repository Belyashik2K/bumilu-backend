from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.favourites.domain.models.favourite import Favourite


class IFavouriteRepository(IBaseRepository[Favourite], ABC):
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
        user_id: UserIdVO,
    ) -> list[Favourite]: ...
