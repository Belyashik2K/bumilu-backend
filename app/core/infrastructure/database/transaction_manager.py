from types import TracebackType
from typing import (
    Self,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.interfaces.transaction_manager import ITransactionManager


class SQLAlchemyTransactionManager(ITransactionManager):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self._rollback()
        else:
            await self._commit()
        await self._close()

    async def _commit(self) -> None:
        if self._session:
            await self._session.commit()

    async def _rollback(self) -> None:
        if self._session:
            await self._session.rollback()

    async def _close(self) -> None:
        if self._session:
            await self._session.close()
