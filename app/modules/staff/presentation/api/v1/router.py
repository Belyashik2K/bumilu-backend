from fastapi import APIRouter
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint

staff_router = APIRouter(
    prefix="/staff",
    tags=["Staff"],
)


@staff_router.get(
    "/me", responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED)
)
async def get_current_staff_member() -> None:
    raise NotImplementedError("Getting current staff member is not implemented yet")
