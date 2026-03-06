from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.deps import get_principal
from app.modules.auth.shared.context import Principal
from app.modules.chat.application.use_cases.user.get_info import (
    GetUserActiveChatInfoInputDTO,
    GetUserActiveChatInfoUseCase,
)
from app.modules.chat.application.use_cases.user.get_messages import (
    GetUserActiveChatMessagesInputDTO,
    GetUserActiveChatMessagesUseCase,
)
from app.modules.chat.application.use_cases.user.submit_message import (
    SubmitUserMessageInputDTO,
    SubmitUserMessageUseCase,
)
from app.modules.chat.presentation.api.schemas.get import (
    GetChatInfoResponseSchema,
    GetChatMessagesResponseSchema,
)
from app.modules.chat.presentation.api.schemas.submit import (
    SubmitUserMessageRequestSchema,
    SubmitUserMessageResponseSchema,
)

chat_router = APIRouter(tags=["Chat"], dependencies=[Depends(security)])


@chat_router.post(
    "/users/me/chat",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def submit_user_message(
    uc: FromDishka[SubmitUserMessageUseCase],
    data: SubmitUserMessageRequestSchema,
    principal: Annotated[Principal, Depends(get_principal)],
) -> SubmitUserMessageResponseSchema:
    result = await uc(
        SubmitUserMessageInputDTO(
            user_id=principal.id.value,
            text=data.text,
            latitude=data.location.latitude if data.location else None,
            longitude=data.location.longitude if data.location else None,
        )
    )
    return SubmitUserMessageResponseSchema.model_validate(result, from_attributes=True)


@chat_router.get(
    "/users/me/chat",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_current_user_chat(
    uc: FromDishka[GetUserActiveChatInfoUseCase],
    principal: Annotated[Principal, Depends(get_principal)],
) -> GetChatInfoResponseSchema:
    result = await uc(
        GetUserActiveChatInfoInputDTO(
            user_id=principal.id.value,
        )
    )
    return GetChatInfoResponseSchema.model_validate(result, from_attributes=True)


@chat_router.get(
    "/users/me/chat/messages",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_current_user_chat_messages(
    uc: FromDishka[GetUserActiveChatMessagesUseCase],
    principal: Annotated[Principal, Depends(get_principal)],
) -> GetChatMessagesResponseSchema:
    result = await uc(
        GetUserActiveChatMessagesInputDTO(
            user_id=principal.id.value,
        )
    )
    return GetChatMessagesResponseSchema.model_validate(result, from_attributes=True)
