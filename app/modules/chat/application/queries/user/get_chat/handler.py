from app.core.application.queries import IQueryHandler
from app.modules.chat.application.queries.shared.readers import IChatReader
from app.modules.chat.application.queries.user.get_chat.query import (
    GetUserRecentChatQuery,
)
from app.modules.chat.application.queries.user.get_chat.view import UserChatView


class GetUserRecentChatQueryHandler(
    IQueryHandler[GetUserRecentChatQuery, UserChatView | None]
):
    def __init__(
        self,
        chat_reader: IChatReader,
    ) -> None:
        self._chat_reader = chat_reader

    async def handle(self, query: GetUserRecentChatQuery) -> UserChatView | None:
        return await self._chat_reader.get_recent_chat_by_user_id(user_id=query.user_id)
