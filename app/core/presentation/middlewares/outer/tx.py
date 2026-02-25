from collections.abc import (
    Awaitable,
    Callable,
)

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.core.presentation.custom_request import CustomRequest
from app.core.presentation.middlewares import CustomBaseHTTPMiddleware


class SQLAlchemyTransactionMiddleware(CustomBaseHTTPMiddleware):
    async def dispatch(
        self,
        request: CustomRequest,
        call_next: Callable[[CustomRequest], Awaitable[Response]],
    ) -> Response:
        try:
            response = await call_next(request)
        except Exception:
            session = await self.get_dependency(request, AsyncSession)
            await session.rollback()
            raise
        else:
            session = await self.get_dependency(request, AsyncSession)
            if response.status_code >= 400:
                await session.rollback()
            else:
                await session.commit()
            return response
