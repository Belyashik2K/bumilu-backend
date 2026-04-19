from app.core.application.queries import IQueryHandler
from app.modules.chat.application.queries.admin.get_chat.query import (
    GetAdminChatQuery,
)
from app.modules.chat.application.queries.admin.get_chat.view import AdminChatView
from app.modules.chat.application.queries.shared.readers import IChatReader
from app.modules.chat.application.shared.exceptions import ChatNotFound


class GetAdminChatQueryHandler(IQueryHandler[GetAdminChatQuery, AdminChatView]):
    def __init__(
        self,
        chat_reader: IChatReader,
    ) -> None:
        self._chat_reader = chat_reader

    async def handle(self, query: GetAdminChatQuery) -> AdminChatView:
        chat = await self._chat_reader.get_admin_chat_by_id(query.chat_id)
        if chat is None:
            # TODO: use proper exception handling
            raise ChatNotFound(chat_id=query.chat_id)  # type: ignore

        return chat
