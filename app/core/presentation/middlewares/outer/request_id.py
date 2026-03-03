from starlette.middleware.base import BaseHTTPMiddleware

from app.core.infrastructure.logging.context import (
    generate_request_id,
    request_id_ctx,
)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(generate_request_id())
        token = request_id_ctx.set(request_id)

        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            request_id_ctx.reset(token)
