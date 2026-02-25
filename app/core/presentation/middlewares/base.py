from collections.abc import Awaitable, Callable
from typing import TypeVar

from dishka import AsyncContainer
from fastapi import FastAPI, Request
from starlette.datastructures import State
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

T = TypeVar("T")


class CustomBaseHTTPMiddleware(BaseHTTPMiddleware):
    """
    Base middleware class that supports dependency injection.

    Inherit from this class to create middlewares that can have dependencies
    injected through the dishka container.

    Use the `get_dependency()` method to resolve dependencies from the container.
    """

    def __init__(
        self,
        app: ASGIApp,
        dispatch: Callable[
            [Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]
        ]
        | None = None,
    ) -> None:
        """
        Initialize the middleware.

        Args:
            app: The ASGI application
            dispatch: Optional custom dispatch function
        """
        super().__init__(app, dispatch=dispatch)

    @staticmethod
    async def get_dependency(request: Request, dependency_type: type[T]) -> T:
        """
        Get a dependency from the dishka container.

        This method first tries to get the dependency from the request-scoped container
        (which can access both REQUEST and APP scoped dependencies), and falls back
        to the app-scoped container if the request container is not available.

        Args:
            request: The current request (used to access the container)
            dependency_type: The type of dependency to resolve

        Returns:
            The resolved dependency instance

        Raises:
            AttributeError: If no container is available
        """

        container: AsyncContainer

        app: FastAPI = request.app
        request_state: State = request.state
        app_state: State = app.state  # type: ignore

        # Try to get from request container first (can access REQUEST + APP scopes)
        if hasattr(request_state, "dishka_container"):
            container = request_state.dishka_container
            assert container is not None

            result = await container.get(dependency_type)

            return result

        # Fallback to app container (APP scope only)
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
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Process the request and response.

        Override this method in your middleware to implement custom logic.
        Use `await self.get_dependency(request, SomeClass)` to get dependencies.

        Args:
            request: The incoming request
            call_next: Function to call the next middleware/endpoint

        Returns:
            The response object
        """
        # Default implementation just passes through
        return await call_next(request)
