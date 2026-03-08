from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.deps import (
    get_admin_principal,
)
from app.modules.auth.shared.context import Principal
from app.modules.chat.application.commands.admin import (
    SubmitAdminMessageCommand,
    SubmitAdminMessageCommandHandler,
)
from app.modules.chat.presentation.api.schemas.common import CHAT_ID_PATH
from app.modules.chat.presentation.api.schemas.submit import (
    SubmitAdminMessageRequestSchema,
    SubmitAdminMessageResponseSchema,
)

admin_chat_router = APIRouter(
    prefix="/admin/chats", tags=["Admin Chats"], dependencies=[Depends(security)]
)


@admin_chat_router.get(
    "",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def get_chats_list() -> None:
    raise NotImplementedError("This endpoint is not implemented yet.")


@admin_chat_router.get(
    "/{chat_id}",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def get_chat_info(chat_id: UUID7 = CHAT_ID_PATH) -> None:
    raise NotImplementedError("This endpoint is not implemented yet.")


@admin_chat_router.get(
    "/{chat_id}/messages",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def get_chat_messages(chat_id: UUID7 = CHAT_ID_PATH) -> None:
    raise NotImplementedError("This endpoint is not implemented yet.")


@admin_chat_router.post(
    "/{chat_id}/close",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def close_chat_as_admin(chat_id: UUID7 = CHAT_ID_PATH) -> None:
    raise NotImplementedError("This endpoint is not implemented yet.")


@admin_chat_router.post("/{chat_id}/reply")
@inject
async def reply_to_chat_as_admin(
    handler: FromDishka[SubmitAdminMessageCommandHandler],
    data: SubmitAdminMessageRequestSchema,
    principal: Principal = Depends(get_admin_principal),
    chat_id: UUID7 = CHAT_ID_PATH,
) -> SubmitAdminMessageResponseSchema:
    result = await handler(
        SubmitAdminMessageCommand(
            actor_id=principal.id.value, chat_id=chat_id, text=data.text
        )
    )
    return SubmitAdminMessageResponseSchema(message_id=result.message_id)
