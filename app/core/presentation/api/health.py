from fastapi import APIRouter

from app.core.presentation.api.schemas.healthcheck import HealthCheckResponse

health_router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@health_router.get("")
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")
