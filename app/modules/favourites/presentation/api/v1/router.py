from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security

favourites_router = APIRouter(
    tags=["Favourites"],
    dependencies=[Depends(security)],
)


@favourites_router.get(
    "/users/me/favourites",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
async def get_my_favourites() -> None:
    raise NotImplementedError()


@favourites_router.get(
    "/users/{user_id}/favourites",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
async def get_favourites_by_user_id() -> None:
    raise NotImplementedError()


@favourites_router.put(
    "/users/me/favourites/{entity_type}/{entity_id}",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
async def add_to_favourites() -> None:
    raise NotImplementedError()


@favourites_router.delete(
    "/users/me/favourites/{entity_type}/{entity_id}",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
async def remove_from_favourites() -> None:
    raise NotImplementedError()
