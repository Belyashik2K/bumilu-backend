from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint

staff_auth_router = APIRouter(tags=["Staff Auth"], prefix="/staff")


@staff_auth_router.post(
    "/login",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def staff_login() -> None:
    raise NotImplementedError("Staff login is not implemented yet")


@staff_auth_router.post(
    "/refresh",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
async def staff_refresh() -> None:
    raise NotImplementedError("Staff refresh is not implemented yet")


@staff_auth_router.post(
    "/logout",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def staff_logout() -> None:
    raise NotImplementedError("Staff logout is not implemented yet")
