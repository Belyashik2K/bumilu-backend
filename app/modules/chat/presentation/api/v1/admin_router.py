from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7

from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.deps import get_principal
from app.modules.auth.shared.context import Principal
from app.modules.chat.application.use_cases.admin.submit_message import (
    SubmitAdminMessageInputDTO,
    SubmitAdminMessageUseCase,
)
from app.modules.chat.presentation.api.schemas.common import CHAT_ID_PATH
from app.modules.chat.presentation.api.schemas.submit import (
    SubmitAdminMessageRequestSchema,
    SubmitAdminMessageResponseSchema,
)

admin_chat_router = APIRouter(
    prefix="/admin/chats", tags=["Admin Chats"], dependencies=[Depends(security)]
)


@admin_chat_router.post("/{chat_id}/reply")
@inject
async def reply_to_chat_as_admin(
    uc: FromDishka[SubmitAdminMessageUseCase],
    data: SubmitAdminMessageRequestSchema,
    principal: Principal = Depends(get_principal),
    chat_id: UUID7 = CHAT_ID_PATH,
) -> SubmitAdminMessageResponseSchema:
    result = await uc(
        SubmitAdminMessageInputDTO(
            actor_id=principal.id.value, chat_id=chat_id, text=data.text
        )
    )
    return SubmitAdminMessageResponseSchema(message_id=result.message_id)
