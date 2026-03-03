from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.infrastructure.database.exception_catcher import (
    sqlalchemy_exception_catcher,
)
from app.core.infrastructure.database.mixins import PKUUIDMixin
from app.core.shared.domain.value_objects.id import IdVO

TEntity = TypeVar("TEntity")  # Entity
TModel = TypeVar("TModel", bound=PKUUIDMixin)  # SQLAlchemy model


class SQLAlchemyBaseRepository(IBaseRepository[TEntity], Generic[TEntity, TModel], ABC):
    def __init__(self, session: AsyncSession, model_class: type[TModel]):
        self.session = session
        self.model_class = model_class  # must be SQLAlchemy declarative model

    @abstractmethod
    def _to_entity(self, data: TModel) -> TEntity: ...

    @abstractmethod
    def _to_data(self, entity: TEntity) -> TModel: ...

    async def _raw_get(self, _id: IdVO) -> TModel | None:
        stmt = select(self.model_class).where(self.model_class.id == _id.value)
        result = await self.session.execute(stmt)
        data = result.scalar_one_or_none()
        return data

    @sqlalchemy_exception_catcher
    async def save(self, entity: TEntity) -> TEntity:  # TODO: split into add and save
        data = self._to_data(entity)
        merged_data = await self.session.merge(data)
        await self.session.flush()
        return self._to_entity(merged_data)

    @sqlalchemy_exception_catcher
    async def get_by_id(self, _id: IdVO) -> TEntity | None:
        if not (data := await self._raw_get(_id)):
            return None
        return self._to_entity(data)
