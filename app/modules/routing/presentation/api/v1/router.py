from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security

routing_router = APIRouter(
    prefix="/routing",
    tags=["Routing"],
    dependencies=[Depends(security)],
)


@routing_router.get(
    "/route", responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED)
)
async def get_route_between_points() -> None:
    return None
