from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.shared.domain.value_objects.id import ChatIdVO
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.commands.answer_with_ai.command import (
    AnswerWithAIInChatCommand,
)
from app.modules.chat.application.interfaces.chat_responder import IChatResponder
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.chat.domain.value_objects.message_text import MessageTextVO


class AnswerWithAIInChatCommandHandler(ICommandHandler[AnswerWithAIInChatCommand]):
    def __init__(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
        chat_responder: IChatResponder,
        transaction_manager: ITransactionManager,
        confidence_score_threshold: float,
    ) -> None:
        super().__init__(transaction_manager)
        self._chat_repository = chat_repository
        self._chat_message_repository = chat_message_repository
        self._chat_responder = chat_responder
        self._confidence_score_threshold = confidence_score_threshold

    async def handle(self, command: AnswerWithAIInChatCommand) -> None:
        now = get_current_dt()
        chat_id = ChatIdVO.from_uuid(command.chat_id)

        # TODO: Change status to PROCESSING_WITH_AI and release lock, start new transaction
        chat = await self._chat_repository.get_by_id_with_lock(chat_id)
        if chat is None:
            print(f"Chat with id {chat_id} not found or locked by other process")
            return None

        if command.expected_last_activity_at != chat.last_activity_at:
            print(
                f"Chat with id {chat_id} has been updated since the command was issued, skipping AI response"
            )
            return None

        chat_messages = await self._chat_message_repository.get_chat_messages(chat_id)

        try:
            result = await self._chat_responder.generate_reply(chat, chat_messages)

            if result.confidence_score < self._confidence_score_threshold:
                chat.escalate_to_admin(now=now)
            else:
                message_text = MessageTextVO(result.reply)
                reply = chat.reply_as_ai(text=message_text, now=now)
                await self._chat_message_repository.save(reply)

            await self._chat_repository.save(chat)
        except Exception:  # TODO: add specific exception for chat responder errors
            chat.escalate_to_admin(now=now)
            await self._chat_repository.save(chat)

        return None
