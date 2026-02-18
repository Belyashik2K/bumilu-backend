from fastapi import APIRouter

from app.core.presentation.api.v1.schemas import HealthCheckResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(
        status="ok"
    )
