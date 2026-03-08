from typing import (
    Annotated,
)

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.core.shared.presentation.schemas.pagination import (
    OffsetPaginationDep,
)
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.deps import (
    get_admin_principal,
)
from app.modules.auth.shared.context import Principal
from app.modules.chat.application.commands.admin import (
    SubmitAdminMessageCommand,
    SubmitAdminMessageCommandHandler,
)
from app.modules.chat.application.commands.admin.close_chat import (
    CloseChatAsAdminCommand,
    CloseChatAsAdminCommandHandler,
)
from app.modules.chat.application.queries.admin.get_chat.handler import (
    GetAdminChatQueryHandler,
)
from app.modules.chat.application.queries.admin.get_chat.query import GetAdminChatQuery
from app.modules.chat.application.queries.admin.get_chat_list.handler import (
    GetAdminChatListQueryHandler,
)
from app.modules.chat.application.queries.admin.get_chat_list.query import (
    GetAdminChatListQuery,
)
from app.modules.chat.application.queries.admin.get_chat_messages.handler import (
    GetAdminChatMessagesQueryHandler,
)
from app.modules.chat.application.queries.admin.get_chat_messages.query import (
    GetAdminChatMessagesQuery,
)
from app.modules.chat.presentation.api.schemas.admin.get import (
    AdminChatFiltersDep,
    AdminChatInfoSchema,
    AdminChatListResponseSchema,
)
from app.modules.chat.presentation.api.schemas.common import CHAT_ID_PATH
from app.modules.chat.presentation.api.schemas.user.get import (
    GetChatMessagesResponseSchema,
)
from app.modules.chat.presentation.api.schemas.user.submit import (
    SubmitAdminMessageRequestSchema,
    SubmitAdminMessageResponseSchema,
)

admin_chat_router = APIRouter(
    prefix="/admin/chats", tags=["Admin Chats"], dependencies=[Depends(security)]
)


@admin_chat_router.get(
    "",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_chats_list(
    handler: FromDishka[GetAdminChatListQueryHandler],
    principal: Annotated[Principal, Depends(get_admin_principal)],
    filters: AdminChatFiltersDep,
    pagination: OffsetPaginationDep,
) -> AdminChatListResponseSchema:
    result = await handler(
        GetAdminChatListQuery(
            actor_id=principal.id.value,
            limit=pagination.limit,
            offset=pagination.offset,
            status=filters.status,
        )
    )
    return AdminChatListResponseSchema.model_validate(result, from_attributes=True)


@admin_chat_router.get(
    "/{chat_id}",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def get_chat_info(
    handler: FromDishka[GetAdminChatQueryHandler],
    principal: Annotated[Principal, Depends(get_admin_principal)],
    chat_id: UUID7 = CHAT_ID_PATH,
) -> AdminChatInfoSchema:
    result = await handler(
        GetAdminChatQuery(
            actor_id=principal.id.value,
            chat_id=chat_id,
        )
    )
    return AdminChatInfoSchema.model_validate(result, from_attributes=True)


@admin_chat_router.get(
    "/{chat_id}/messages",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def get_chat_messages(
    handler: FromDishka[GetAdminChatMessagesQueryHandler],
    principal: Annotated[Principal, Depends(get_admin_principal)],
    pagination: OffsetPaginationDep,
    chat_id: UUID7 = CHAT_ID_PATH,
) -> GetChatMessagesResponseSchema:
    result = await handler(
        GetAdminChatMessagesQuery(
            actor_id=principal.id.value,
            limit=pagination.limit,
            offset=pagination.offset,
            chat_id=chat_id,
        )
    )
    return GetChatMessagesResponseSchema.model_validate(result, from_attributes=True)


@admin_chat_router.post(
    "/{chat_id}/close",
    responses=generate_responses_for_endpoint(status.HTTP_404_NOT_FOUND),
)
@inject
async def close_chat_as_admin(
    handler: FromDishka[CloseChatAsAdminCommandHandler],
    principal: Principal = Depends(get_admin_principal),
    chat_id: UUID7 = CHAT_ID_PATH,
) -> None:
    await handler(CloseChatAsAdminCommand(actor_id=principal.id.value, chat_id=chat_id))


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
