from abc import (
    ABC,
    abstractmethod,
)

from app.core.domain.value_objects.id import (
    IdVO,
    PrincipalIdVO,
)


class IPlaceFavouriteRepository(ABC):
    @abstractmethod
    async def add_if_not_exists(
        self,
        user_id: PrincipalIdVO,
        entity_id: IdVO,
    ) -> None: ...

    @abstractmethod
    async def remove_if_exists(
        self,
        user_id: PrincipalIdVO,
        entity_id: IdVO,
    ) -> None: ...
