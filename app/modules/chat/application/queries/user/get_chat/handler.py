from app.core.application.queries import IQueryHandler
from app.modules.chat.application.queries.readers.chat import IChatReader
from app.modules.chat.application.queries.user.get_chat.query import (
    GetUserActiveChatQuery,
)
from app.modules.chat.application.queries.user.get_chat.view import UserChatView


class GetUserActiveChatQueryHandler(
    IQueryHandler[GetUserActiveChatQuery, UserChatView | None]
):
    def __init__(
        self,
        chat_reader: IChatReader,
    ) -> None:
        self._chat_reader = chat_reader

    async def handle(self, query: GetUserActiveChatQuery) -> UserChatView | None:
        return await self._chat_reader.get_active_chat_by_user_id(user_id=query.user_id)
