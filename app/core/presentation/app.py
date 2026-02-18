from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.core.infrastructure.config import AppConfig
from app.core.presentation.api import api_router


def create_app() -> FastAPI:
    config = AppConfig()  # type: ignore

    app = FastAPI(
        title=config.docs.title,
        description=config.docs.description,
        version=config.docs.version,
        openapi_url=config.docs.openapi_url,
        docs_url=config.docs.swagger_url,
        redoc_url=config.docs.redoc_url,
        default_response_class=ORJSONResponse,
    )

    if config.cors.enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.cors.allow_origins,
            allow_credentials=config.cors.allow_credentials,
            allow_methods=config.cors.allow_methods,
            allow_headers=config.cors.allow_headers,
        )

    app.include_router(api_router)
    return app


app = create_app()
