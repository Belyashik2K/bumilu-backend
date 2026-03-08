from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.core.shared.presentation.schemas.pagination import OffsetPaginationQuery
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.deps import get_principal
from app.modules.auth.shared.context import Principal
from app.modules.chat.application.commands.user import (
    SubmitUserMessageCommand,
    SubmitUserMessageCommandHandler,
)
from app.modules.chat.application.queries.user import (
    GetUserActiveChatMessagesQuery,
    GetUserActiveChatMessagesQueryHandler,
    GetUserActiveChatQuery,
    GetUserActiveChatQueryHandler,
)
from app.modules.chat.presentation.api.schemas.get import (
    GetChatInfoResponseSchema,
    GetChatMessagesResponseSchema,
)
from app.modules.chat.presentation.api.schemas.submit import (
    SubmitUserMessageRequestSchema,
    SubmitUserMessageResponseSchema,
)

user_chat_router = APIRouter(tags=["Chat"], dependencies=[Depends(security)])


@user_chat_router.post(
    "/users/me/chat",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def submit_user_message(
    handler: FromDishka[SubmitUserMessageCommandHandler],
    data: SubmitUserMessageRequestSchema,
    principal: Annotated[Principal, Depends(get_principal)],
) -> SubmitUserMessageResponseSchema:
    result = await handler(
        SubmitUserMessageCommand(
            user_id=principal.id.value,
            text=data.text,
            latitude=data.location.latitude if data.location else None,
            longitude=data.location.longitude if data.location else None,
        )
    )
    return SubmitUserMessageResponseSchema.model_validate(result, from_attributes=True)


@user_chat_router.get(
    "/users/me/chat",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_current_user_chat(
    handler: FromDishka[GetUserActiveChatQueryHandler],
    principal: Annotated[Principal, Depends(get_principal)],
) -> GetChatInfoResponseSchema | dict:
    result = await handler(
        GetUserActiveChatQuery(
            user_id=principal.id.value,
        )
    )
    return (
        GetChatInfoResponseSchema.model_validate(result, from_attributes=True)
        if result
        else {}
    )


@user_chat_router.get(
    "/users/me/chat/messages",
    responses=generate_responses_for_endpoint(),
    response_model_exclude_none=True,
)
@inject
async def get_current_user_chat_messages(
    handler: FromDishka[GetUserActiveChatMessagesQueryHandler],
    principal: Annotated[Principal, Depends(get_principal)],
    pagination: Annotated[OffsetPaginationQuery, Query()],
) -> GetChatMessagesResponseSchema | dict:
    result = await handler(
        GetUserActiveChatMessagesQuery(
            user_id=principal.id.value,
            limit=pagination.limit,
            offset=pagination.offset,
        )
    )
    return (
        GetChatMessagesResponseSchema.model_validate(result, from_attributes=True)
        if result
        else {}
    )
