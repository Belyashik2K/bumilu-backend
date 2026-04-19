from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)

from app.core.domain.value_objects.id import IdVO

TEntity = TypeVar("TEntity")


class IBaseRepository(Generic[TEntity], ABC):
    @abstractmethod
    async def save(self, entity: TEntity) -> TEntity: ...

    @abstractmethod
    async def batch_save(self, entities: list[TEntity]) -> list[TEntity]: ...

    @abstractmethod
    async def get_by_id(self, _id: IdVO) -> TEntity | None: ...
