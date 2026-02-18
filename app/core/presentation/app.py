from fastapi import (
    FastAPI
)

from app.core.presentation.api import router as api_router

app = FastAPI(
    title="BumiLu API",
    description="API for BumiLu application",
    version="1.0.0",
)
app.include_router(api_router)
