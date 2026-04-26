from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.infrastructure.config import AppConfig
from app.modules.chat.application.commands.admin import SubmitAdminMessageCommandHandler
from app.modules.chat.application.commands.admin.close_chat import (
    CloseChatAsAdminCommandHandler,
)
from app.modules.chat.application.commands.answer_with_ai.handler import (
    AnswerWithAIInChatCommandHandler,
)
from app.modules.chat.application.commands.cron import (
    CloseInactiveChatsCommandHandler,
)
from app.modules.chat.application.commands.user import SubmitUserMessageCommandHandler
from app.modules.chat.application.interfaces.chat_reply_dispatcher import (
    IChatReplyDispatcher,
)
from app.modules.chat.application.interfaces.chat_responder import IChatResponder
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.users.application.interfaces.repositories.user import IUserRepository


class ChatCommandHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def submit_user_message_handler(
        self,
        config: AppConfig,
        user_repository: IUserRepository,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
        chat_reply_dispatcher: IChatReplyDispatcher,
        transaction_manager: ITransactionManager,
    ) -> SubmitUserMessageCommandHandler:
        return SubmitUserMessageCommandHandler(
            ai_answer_delay_seconds=config.chat.ai_assistant.answer_delay_sec,
            transaction_manager=transaction_manager,
            user_repository=user_repository,
            chat_repository=chat_repository,
            chat_message_repository=chat_message_repository,
            chat_reply_dispatcher=chat_reply_dispatcher,
        )

    @provide(scope=Scope.REQUEST)
    async def submit_admin_reply_handler(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
        transaction_manager: ITransactionManager,
    ) -> SubmitAdminMessageCommandHandler:
        return SubmitAdminMessageCommandHandler(
            transaction_manager=transaction_manager,
            chat_repository=chat_repository,
            chat_message_repository=chat_message_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def close_inactive_chats_handler(
        self,
        config: AppConfig,
        chat_repository: IChatRepository,
        transaction_manager: ITransactionManager,
    ) -> CloseInactiveChatsCommandHandler:
        return CloseInactiveChatsCommandHandler(
            transaction_manager=transaction_manager,
            chat_repository=chat_repository,
            inactivity_threshold_minutes=config.chat.inactivity.threshold_min,
        )

    @provide(scope=Scope.REQUEST)
    async def close_chat_as_admin_handler(
        self,
        chat_repository: IChatRepository,
        transaction_manager: ITransactionManager,
    ) -> CloseChatAsAdminCommandHandler:
        return CloseChatAsAdminCommandHandler(
            transaction_manager=transaction_manager,
            chat_repository=chat_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def answer_as_ai_in_chat_handler(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
        transaction_manager: ITransactionManager,
        chat_responder: IChatResponder,
        config: AppConfig,
    ) -> AnswerWithAIInChatCommandHandler:
        return AnswerWithAIInChatCommandHandler(
            transaction_manager=transaction_manager,
            chat_repository=chat_repository,
            chat_message_repository=chat_message_repository,
            chat_responder=chat_responder,
            confidence_score_threshold=config.chat.ai_assistant.confidence_score_threshold,
        )
