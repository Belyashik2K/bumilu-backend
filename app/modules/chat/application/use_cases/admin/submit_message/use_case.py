from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import (
    ChatIdVO,
    UserIdVO,
)
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.chat.application.use_cases.admin.submit_message import (
    SubmitAdminMessageInputDTO,
    SubmitAdminMessageOutputDTO,
)
from app.modules.chat.application.use_cases.shared.exceptions import ChatNotFound
from app.modules.chat.domain.value_objects.message_text import MessageTextVO


class SubmitAdminMessageUseCase(
    IBaseUseCase[
        SubmitAdminMessageInputDTO,
        SubmitAdminMessageOutputDTO,
    ]
):
    def __init__(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
    ) -> None:
        self._chat_repository = chat_repository
        self._chat_message_repository = chat_message_repository

    async def execute(
        self,
        input_data: SubmitAdminMessageInputDTO,
    ) -> SubmitAdminMessageOutputDTO:
        author_id = UserIdVO.from_uuid(input_data.actor_id)
        chat_id = ChatIdVO.from_uuid(input_data.chat_id)
        text = MessageTextVO(input_data.text)
        now = get_current_dt()

        chat = await self._chat_repository.get_by_id(chat_id)
        if not chat:
            raise ChatNotFound(chat_id=chat_id)

        # We believe that only admins can call this use case,
        # but later we might want to add a check here to ensure that the actor is indeed an admin.
        message = chat.reply_as_admin(author_id=author_id, text=text, now=now)

        await self._chat_repository.save(chat)
        await self._chat_message_repository.save(message)

        return SubmitAdminMessageOutputDTO(
            message_id=message.id.value,
        )
