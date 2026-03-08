from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.config import AppConfig
from app.modules.chat.application.commands.admin import (
    SubmitAdminMessageCommandHandler,
)
from app.modules.chat.application.commands.admin.close_chat import (
    CloseChatAsAdminCommandHandler,
)
from app.modules.chat.application.commands.cron import (
    CloseInactiveChatsCommandHandler,
    ProcessPendingChatsCommandHandler,
)
from app.modules.chat.application.commands.user.submit_message import (
    SubmitUserMessageCommandHandler,
)
from app.modules.chat.application.interfaces.chat_responder import IChatResponder
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.chat.application.queries.admin.get_chat.handler import (
    GetAdminChatQueryHandler,
)
from app.modules.chat.application.queries.admin.get_chat_list.handler import (
    GetAdminChatListQueryHandler,
)
from app.modules.chat.application.queries.admin.get_chat_messages.handler import (
    GetAdminChatMessagesQueryHandler,
)
from app.modules.chat.application.queries.readers.chat import IChatReader
from app.modules.chat.application.queries.readers.chat_message import IChatMessageReader
from app.modules.chat.application.queries.user import (
    GetUserActiveChatMessagesQueryHandler,
    GetUserActiveChatQueryHandler,
)
from app.modules.chat.infrastructure.chat_responders.openrouter import (
    OpenRouterChatResponder,
)
from app.modules.chat.infrastructure.database.readers.chat import SQLAlchemyChatReader
from app.modules.chat.infrastructure.database.readers.chat_message import (
    SQLAlchemyChatMessageReader,
)
from app.modules.chat.infrastructure.database.repositories.chat import (
    SQLAlchemyChatRepository,
)
from app.modules.chat.infrastructure.database.repositories.chat_message import (
    SQLAlchemyChatMessageRepository,
)
from app.modules.users.application.interfaces.repositories.user import IUserRepository


class ChatProvider(Provider):
    @provide(scope=Scope.APP, provides=IChatResponder)
    def chat_responder(
        self,
        config: AppConfig,
    ) -> OpenRouterChatResponder:
        return OpenRouterChatResponder(
            api_key=config.chat.ai_assistant.openrouter.api_key,
            api_base_url=config.chat.ai_assistant.openrouter.api_base_url,
            model=config.chat.ai_assistant.openrouter.model,
            system_prompt=config.chat.ai_assistant.system_prompt,
        )

    @provide(scope=Scope.REQUEST, provides=IChatRepository)
    async def chat_repository(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyChatRepository:
        return SQLAlchemyChatRepository(
            session=session,
        )

    @provide(scope=Scope.REQUEST, provides=IChatReader)
    async def chat_reader(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyChatReader:
        return SQLAlchemyChatReader(
            session=session,
        )

    @provide(scope=Scope.REQUEST, provides=IChatMessageRepository)
    async def chat_message_repository(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyChatMessageRepository:
        return SQLAlchemyChatMessageRepository(
            session=session,
        )

    @provide(scope=Scope.REQUEST, provides=IChatMessageReader)
    async def chat_message_reader(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyChatMessageReader:
        return SQLAlchemyChatMessageReader(
            session=session,
        )

    @provide(scope=Scope.REQUEST)
    async def get_user_active_chat_info_handler(
        self,
        chat_reader: IChatReader,
    ) -> GetUserActiveChatQueryHandler:
        return GetUserActiveChatQueryHandler(
            chat_reader=chat_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_user_active_chat_messages_handler(
        self, chat_reader: IChatReader, chat_message_reader: IChatMessageReader
    ) -> GetUserActiveChatMessagesQueryHandler:
        return GetUserActiveChatMessagesQueryHandler(
            chat_reader=chat_reader,
            chat_message_reader=chat_message_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def submit_user_message_handler(
        self,
        user_repository: IUserRepository,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
    ) -> SubmitUserMessageCommandHandler:
        return SubmitUserMessageCommandHandler(
            user_repository=user_repository,
            chat_repository=chat_repository,
            chat_message_repository=chat_message_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def process_pending_chats_handler(
        self,
        config: AppConfig,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
        chat_responder: IChatResponder,
    ) -> ProcessPendingChatsCommandHandler:
        return ProcessPendingChatsCommandHandler(
            chat_repository=chat_repository,
            chat_message_repository=chat_message_repository,
            chat_responder=chat_responder,
            confidence_score_threshold=config.chat.ai_assistant.confidence_score_threshold,
        )

    @provide(scope=Scope.REQUEST)
    async def submit_admin_reply_handler(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
    ) -> SubmitAdminMessageCommandHandler:
        return SubmitAdminMessageCommandHandler(
            chat_repository=chat_repository,
            chat_message_repository=chat_message_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def close_inactive_chats_handler(
        self,
        config: AppConfig,
        chat_repository: IChatRepository,
    ) -> CloseInactiveChatsCommandHandler:
        return CloseInactiveChatsCommandHandler(
            chat_repository=chat_repository,
            inactivity_threshold_minutes=config.chat.inactivity.threshold_min,
        )

    @provide(scope=Scope.REQUEST)
    async def close_chat_as_admin_handler(
        self,
        chat_repository: IChatRepository,
    ) -> CloseChatAsAdminCommandHandler:
        return CloseChatAsAdminCommandHandler(chat_repository=chat_repository)

    @provide(scope=Scope.REQUEST)
    async def get_admin_chat_list_handler(
        self,
        chat_reader: IChatReader,
    ) -> GetAdminChatListQueryHandler:
        return GetAdminChatListQueryHandler(chat_reader=chat_reader)

    @provide(scope=Scope.REQUEST)
    async def get_admin_chat_handler(
        self,
        chat_reader: IChatReader,
    ) -> GetAdminChatQueryHandler:
        return GetAdminChatQueryHandler(chat_reader=chat_reader)

    @provide(scope=Scope.REQUEST)
    async def get_admin_chat_messages_handler(
        self,
        chat_reader: IChatReader,
        chat_message_reader: IChatMessageReader,
    ) -> GetAdminChatMessagesQueryHandler:
        return GetAdminChatMessagesQueryHandler(
            chat_reader=chat_reader,
            chat_message_reader=chat_message_reader,
        )
