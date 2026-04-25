from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7
from starlette import status
from starlette.responses import Response

from app.core.presentation.api.schemas.pagination import (
    OffsetPaginationDep,
)
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.users.deps import get_user_principal
from app.modules.auth.shared.context import Principal
from app.modules.chat.application.commands.user import (
    SubmitUserMessageCommand,
    SubmitUserMessageCommandHandler,
)
from app.modules.chat.application.queries.user.get_chat.handler import (
    GetUserRecentChatQueryHandler,
)
from app.modules.chat.application.queries.user.get_chat.query import (
    GetUserRecentChatQuery,
)
from app.modules.chat.application.queries.user.get_messages.handler import (
    GetUserRecentChatMessagesQueryHandler,
)
from app.modules.chat.application.queries.user.get_messages.query import (
    GetUserRecentChatMessagesQuery,
)
from app.modules.chat.presentation.api.schemas.user.get import (
    GetChatInfoResponseSchema,
    GetChatMessagesResponseSchema,
)
from app.modules.chat.presentation.api.schemas.user.submit import (
    SubmitUserMessageRequestSchema,
    SubmitUserMessageResponseSchema,
)

user_chat_router = APIRouter(tags=["Chat"], dependencies=[Depends(security)])


@user_chat_router.post(
    "/users/me/chat",
    status_code=status.HTTP_201_CREATED,
    responses=generate_responses_for_endpoint(),
)
@inject
async def submit_user_message(
    handler: FromDishka[SubmitUserMessageCommandHandler],
    data: SubmitUserMessageRequestSchema,
    principal: Annotated[Principal, Depends(get_user_principal)],
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
    responses=generate_responses_for_endpoint(status.HTTP_204_NO_CONTENT),
)
@inject
async def get_recent_user_chat(
    handler: FromDishka[GetUserRecentChatQueryHandler],
    principal: Annotated[Principal, Depends(get_user_principal)],
) -> GetChatInfoResponseSchema | None:
    result = await handler(
        GetUserRecentChatQuery(
            user_id=principal.id.value,
        )
    )
    if not result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)  # type: ignore
    return GetChatInfoResponseSchema.model_validate(result, from_attributes=True)


@user_chat_router.get(
    "/users/me/chat/messages",
    responses=generate_responses_for_endpoint(status.HTTP_204_NO_CONTENT),
)
@inject
async def get_recent_user_chat_messages(
    handler: FromDishka[GetUserRecentChatMessagesQueryHandler],
    principal: Annotated[Principal, Depends(get_user_principal)],
    pagination: OffsetPaginationDep,
    after_message_id: UUID7 | None = None,
) -> GetChatMessagesResponseSchema | None:
    result = await handler(
        GetUserRecentChatMessagesQuery(
            user_id=principal.id.value,
            limit=pagination.limit,
            offset=pagination.offset,
            after_message_id=after_message_id,
        )
    )
    if not result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)  # type: ignore
    return GetChatMessagesResponseSchema.model_validate(result, from_attributes=True)
