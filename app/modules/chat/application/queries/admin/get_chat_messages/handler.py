from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.chat.application.queries.admin.get_chat_messages.query import (
    GetAdminChatMessagesQuery,
)
from app.modules.chat.application.queries.shared.readers import (
    IChatMessageReader,
    IChatReader,
)
from app.modules.chat.application.queries.shared.views import PaginatedChatMessagesView
from app.modules.chat.application.shared.exceptions import ChatNotFound


class GetAdminChatMessagesQueryHandler(
    IQueryHandler[GetAdminChatMessagesQuery, PaginatedChatMessagesView],
):
    def __init__(
        self,
        chat_reader: IChatReader,
        chat_message_reader: IChatMessageReader,
    ) -> None:
        self._chat_reader = chat_reader
        self._chat_message_reader = chat_message_reader

    async def handle(
        self, query: GetAdminChatMessagesQuery
    ) -> PaginatedChatMessagesView:
        chat = await self._chat_reader.get_admin_chat_by_id(query.chat_id)
        if chat is None:
            # TODO: use proper exception handling
            raise ChatNotFound(chat_id=query.chat_id)  # type: ignore

        messages = await self._chat_message_reader.list_messages_by_chat_id(
            chat.id, limit=query.limit, offset=query.offset
        )

        return PaginatedChatMessagesView(
            chat_id=chat.id,
            messages=messages.items,
            pagination=OffsetPagination.create(
                limit=query.limit,
                offset=query.offset,
                total=messages.total,
            ),
        )
