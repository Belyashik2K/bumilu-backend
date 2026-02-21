from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)

TEntity = TypeVar("TEntity")
TId = TypeVar("TId")


class IBaseRepository(Generic[TEntity, TId], ABC):
    @abstractmethod
    async def save(self, entity: TEntity) -> TEntity: ...

    @abstractmethod
    async def get_by_id(self, _id: TId) -> TEntity | None: ...
