from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import (
    FastapiProvider,
    setup_dishka,
)
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.di import CoreProvider
from app.core.infrastructure.config import AppConfig
from app.core.presentation.api import api_router
from app.core.presentation.exceptions import set_exception_handlers
from app.core.presentation.middlewares.outer import SQLAlchemyTransactionMiddleware
from app.modules.auth.di import AuthProvider
from app.modules.users.di import UserProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()  # type: ignore[attr-defined]


def create_app() -> FastAPI:
    config = AppConfig()  # type: ignore[call-arg]

    app = FastAPI(
        title=config.docs.title,
        description=config.docs.description,
        version=config.docs.version,
        openapi_url=config.docs.urls.openapi,
        docs_url=config.docs.urls.swagger,
        redoc_url=config.docs.urls.redoc,
        lifespan=lifespan,
    )

    app.add_middleware(SQLAlchemyTransactionMiddleware)
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
        CoreProvider(), UserProvider(), AuthProvider(), FastapiProvider()
    )
    setup_dishka(container=container, app=app)

    return app


app = create_app()
