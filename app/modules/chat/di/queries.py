from dishka import (
    Provider,
    Scope,
    provide,
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
from app.modules.chat.application.queries.user.get_chat.handler import (
    GetUserActiveChatQueryHandler,
)
from app.modules.chat.application.queries.user.get_messages.handler import (
    GetUserActiveChatMessagesQueryHandler,
)


class ChatQueryHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_active_chat_info_handler(
        self,
        chat_reader: IChatReader,
    ) -> GetUserActiveChatQueryHandler:
        return GetUserActiveChatQueryHandler(chat_reader=chat_reader)

    @provide(scope=Scope.REQUEST)
    async def get_user_active_chat_messages_handler(
        self,
        chat_reader: IChatReader,
        chat_message_reader: IChatMessageReader,
    ) -> GetUserActiveChatMessagesQueryHandler:
        return GetUserActiveChatMessagesQueryHandler(
            chat_reader=chat_reader,
            chat_message_reader=chat_message_reader,
        )

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
