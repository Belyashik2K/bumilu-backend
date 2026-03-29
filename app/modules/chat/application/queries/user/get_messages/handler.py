from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.chat.application.queries.common_views import PaginatedChatMessagesView
from app.modules.chat.application.queries.readers.chat import IChatReader
from app.modules.chat.application.queries.readers.chat_message import IChatMessageReader
from app.modules.chat.application.queries.user.get_messages.query import (
    GetUserRecentChatMessagesQuery,
)


class GetUserRecentChatMessagesQueryHandler(
    IQueryHandler[
        GetUserRecentChatMessagesQuery,
        PaginatedChatMessagesView | None,
    ]
):
    def __init__(
        self,
        chat_reader: IChatReader,
        chat_message_reader: IChatMessageReader,
    ) -> None:
        self._chat_reader = chat_reader
        self._chat_message_reader = chat_message_reader

    async def handle(
        self, query: GetUserRecentChatMessagesQuery
    ) -> PaginatedChatMessagesView | None:
        chat = await self._chat_reader.get_recent_chat_by_user_id(query.user_id)
        if chat is None:
            return None

        messages_page = await self._chat_message_reader.list_messages_by_chat_id(
            chat.id, limit=query.limit, offset=query.offset
        )

        return PaginatedChatMessagesView(
            chat_id=chat.id,
            messages=messages_page.items,
            pagination=OffsetPagination.create(
                limit=query.limit,
                offset=query.offset,
                total=messages_page.total,
            ),
        )
