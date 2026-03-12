from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import (
    Any,
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_dishka import setup_dishka as setup_dishka_scheduler
from dishka import (
    AsyncContainer,
    make_async_container,
)
from dishka.integrations.fastapi import (
    FastapiProvider,
)
from dishka.integrations.fastapi import (
    setup_dishka as setup_dishka_fastapi,
)
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.core.di import CoreProvider
from app.core.infrastructure.config import AppConfig
from app.core.infrastructure.logging import setup_logging
from app.core.presentation.api import api_router
from app.core.presentation.exceptions import set_exception_handlers
from app.core.presentation.middlewares.outer import (
    AccessLogMiddleware,
)
from app.modules.auth.di import AuthProvider
from app.modules.auth.presentation.api.middlewares.auth import AuthMiddleware
from app.modules.chat.di import ChatProvider
from app.modules.chat.infrastructure.apscheduler_jobs import register_chat_jobs
from app.modules.favourites.di import FavouriteProvider
from app.modules.reviews.di import ReviewProvider
from app.modules.users.di import UserProvider


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    container: AsyncContainer = app.state.dishka_container  # type: ignore[attr-defined]
    scheduler = await container.get(AsyncIOScheduler)
    config = await container.get(AppConfig)
    setup_dishka_scheduler(container=container, scheduler=scheduler)
    register_chat_jobs(scheduler, config=config)
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown()
        await container.close()


def create_app() -> FastAPI:
    config = AppConfig()  # type: ignore[call-arg]

    setup_logging(
        level=config.logging.level,
        format=config.logging.format,
        datefmt=config.logging.datetime_format,
    )

    app = FastAPI(
        title=config.docs.title,
        description=config.docs.description,
        version=config.docs.version,
        openapi_url=config.docs.urls.openapi,
        docs_url=config.docs.urls.swagger,
        redoc_url=config.docs.urls.redoc,
        lifespan=lifespan,
    )

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs(request: Request) -> RedirectResponse:
        return RedirectResponse(url=config.docs.urls.swagger)

    app.add_middleware(AuthMiddleware)
    app.add_middleware(AccessLogMiddleware)
    if config.cors.enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.cors.allow_origins,
            allow_credentials=config.cors.allow_credentials,
            allow_methods=config.cors.allow_methods,
            allow_headers=config.cors.allow_headers,
        )

    app.include_router(api_router)

    set_exception_handlers(app)

    container = make_async_container(
        CoreProvider(),
        UserProvider(),
        AuthProvider(),
        ReviewProvider(),
        FavouriteProvider(),
        ChatProvider(),
        FastapiProvider(),
    )
    setup_dishka_fastapi(container=container, app=app)

    return app


app = create_app()
