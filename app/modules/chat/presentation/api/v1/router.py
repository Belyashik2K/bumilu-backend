from fastapi import APIRouter
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@chat_router.post(
    "", responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED)
)
async def submit_user_message() -> None:
    raise NotImplementedError("This endpoint is not implemented yet.")


@chat_router.get(
    "", responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED)
)
async def get_current_user_chat() -> None:
    raise NotImplementedError("This endpoint is not implemented yet.")


@chat_router.get(
    "/messages",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
async def get_current_user_chat_messages() -> None:
    raise NotImplementedError("This endpoint is not implemented yet.")
