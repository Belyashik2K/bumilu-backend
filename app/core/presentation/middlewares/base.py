from collections.abc import (
    Awaitable,
    Callable,
)
from typing import TypeVar

from dishka import AsyncContainer
from fastapi import (
    FastAPI,
    Request,
)
from starlette.datastructures import State
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

from app.core.presentation.custom_request import CustomRequest

T = TypeVar("T")


class CustomBaseHTTPMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        dispatch: Callable[
            [CustomRequest, Callable[[CustomRequest], Awaitable[Response]]],
            Awaitable[Response],
        ]
        | None = None,
    ) -> None:
        super().__init__(app, dispatch=dispatch)

    @staticmethod
    async def get_dependency(request: CustomRequest, dependency_type: type[T]) -> T:
        container: AsyncContainer

        app: FastAPI = request.app
        request_state: State = request.state
        app_state: State = app.state  # type: ignore

        if hasattr(request_state, "dishka_container"):
            container = request_state.dishka_container
            assert container is not None

            result = await container.get(dependency_type)

            return result

        elif hasattr(app_state, "container"):
            container = app_state.container
            assert container is not None

            result = await container.get(dependency_type)

            return result

        else:
            raise AttributeError(
                "No dishka container found. Make sure dishka is properly set up with the app."
            )

    async def dispatch(
        self,
        request: CustomRequest,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        return await call_next(request)
