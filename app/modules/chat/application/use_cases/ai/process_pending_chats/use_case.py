from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.interfaces.chat_responder import IChatResponder
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.chat.application.use_cases.ai.process_pending_chats import (
    ProcessPendingChatsInputDTO,
    ProcessPendingChatsOutputDTO,
)
from app.modules.chat.domain.value_objects.message_text import MessageTextVO


class ProcessPendingChatsUseCase(
    IBaseUseCase[ProcessPendingChatsInputDTO, ProcessPendingChatsOutputDTO]
):
    def __init__(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
        chat_responder: IChatResponder,
        confidence_threshold: float,
    ) -> None:
        self._chat_repository = chat_repository
        self._chat_message_repository = chat_message_repository
        self._chat_responder = chat_responder
        self._confidence_threshold = confidence_threshold

    async def execute(
        self, input_data: ProcessPendingChatsInputDTO
    ) -> ProcessPendingChatsOutputDTO:
        pending_chats = await self._chat_repository.get_pending_chats()
        if not pending_chats:
            return ProcessPendingChatsOutputDTO()

        pending_chat_ids = [chat.id for chat in pending_chats]
        pending_chat_messages = (
            await self._chat_message_repository.batch_get_chat_messages(
                pending_chat_ids
            )
        )

        for chat in pending_chats:
            now = get_current_dt()
            try:
                result = await self._chat_responder.generate_reply(
                    chat, pending_chat_messages.get(chat.id, [])
                )
            except Exception:  # TODO: add specific exception for chat responder errors
                chat.escalate_to_admin(now=now)
                await self._chat_repository.save(chat)
                continue

            if result.confidence_score < self._confidence_threshold:
                chat.escalate_to_admin(now=now)
            else:
                message_text = MessageTextVO(result.reply)
                reply = chat.reply_as_ai(text=message_text, now=now)
                await self._chat_message_repository.save(reply)

            await self._chat_repository.save(chat)

        return ProcessPendingChatsOutputDTO()
