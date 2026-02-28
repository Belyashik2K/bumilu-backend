from collections.abc import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import Response

from app.core.presentation.custom_request import CustomRequest
from app.core.presentation.middlewares import CustomBaseHTTPMiddleware
from app.modules.auth.application.interfaces.managers.access_token import (
    IAccessTokenManager,
)
from app.modules.auth.shared.context import Principal


class AuthMiddleware(CustomBaseHTTPMiddleware):
    @staticmethod
    def _get_token_from_header(request: CustomRequest) -> str | None:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        return parts[1]

    async def dispatch(
        self,
        request: CustomRequest,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request.state.principal = None

        token_manager = await self.get_dependency(request, IAccessTokenManager)
        token = self._get_token_from_header(request)

        if not token:
            return await call_next(request)
        try:
            token_info = token_manager.validate_and_decode(token)
            request.state.principal = Principal(
                id=token_info.user_id,
                session_id=token_info.session_id,
                role=token_info.role,
            )
            return await call_next(request)
        except Exception:
            return await call_next(request)
