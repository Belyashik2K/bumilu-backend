from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.config import AppConfig
from app.modules.chat.application.interfaces.chat_responder import IChatResponder
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.chat.application.use_cases.admin.submit_message import (
    SubmitAdminMessageUseCase,
)
from app.modules.chat.application.use_cases.ai.process_pending_chats import (
    ProcessPendingChatsUseCase,
)
from app.modules.chat.application.use_cases.user.get_info import (
    GetUserActiveChatInfoUseCase,
)
from app.modules.chat.application.use_cases.user.get_messages import (
    GetUserActiveChatMessagesUseCase,
)
from app.modules.chat.application.use_cases.user.submit_message import (
    SubmitUserMessageUseCase,
)
from app.modules.chat.infrastructure.chat_responders.openrouter import (
    OpenRouterChatResponder,
)
from app.modules.chat.infrastructure.repositories.chat import SQLAlchemyChatRepository
from app.modules.chat.infrastructure.repositories.chat_message import (
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
            api_key=config.openrouter.api_key,
            api_base_url=config.openrouter.api_base_url,
            model=config.ai_assistant.model,
            system_prompt=config.ai_assistant.system_prompt,
        )

    @provide(scope=Scope.REQUEST, provides=IChatRepository)
    async def chat_repository(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyChatRepository:
        return SQLAlchemyChatRepository(
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

    @provide(scope=Scope.REQUEST)
    async def get_user_active_chat_info_uc(
        self,
        chat_repository: IChatRepository,
    ) -> GetUserActiveChatInfoUseCase:
        return GetUserActiveChatInfoUseCase(
            chat_repository=chat_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def get_user_active_chat_messages_uc(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
    ) -> GetUserActiveChatMessagesUseCase:
        return GetUserActiveChatMessagesUseCase(
            chat_repository=chat_repository,
            chat_message_repository=chat_message_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def submit_user_message_uc(
        self,
        user_repository: IUserRepository,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
    ) -> SubmitUserMessageUseCase:
        return SubmitUserMessageUseCase(
            user_repository=user_repository,
            chat_repository=chat_repository,
            chat_message_repository=chat_message_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def process_pending_chats_uc(
        self,
        config: AppConfig,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
        chat_responder: IChatResponder,
    ) -> ProcessPendingChatsUseCase:
        return ProcessPendingChatsUseCase(
            chat_repository=chat_repository,
            chat_message_repository=chat_message_repository,
            chat_responder=chat_responder,
            confidence_score_threshold=config.ai_assistant.confidence_score_threshold,
        )

    @provide(scope=Scope.REQUEST)
    async def submit_admin_reply_uc(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
    ) -> SubmitAdminMessageUseCase:
        return SubmitAdminMessageUseCase(
            chat_repository=chat_repository,
            chat_message_repository=chat_message_repository,
        )
