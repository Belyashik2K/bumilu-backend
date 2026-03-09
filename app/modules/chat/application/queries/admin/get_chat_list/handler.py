from app.core.application.queries import IQueryHandler
from app.core.shared.application.queries.pagination import OffsetPagination
from app.modules.chat.application.queries.admin.get_chat_list.query import (
    GetAdminChatListQuery,
)
from app.modules.chat.application.queries.admin.get_chat_list.view import (
    PaginatedAdminChatListView,
)
from app.modules.chat.application.queries.readers.chat import IChatReader


class GetAdminChatListQueryHandler(
    IQueryHandler[GetAdminChatListQuery, PaginatedAdminChatListView],
):
    def __init__(
        self,
        chat_reader: IChatReader,
    ) -> None:
        self._chat_reader = chat_reader

    async def handle(self, query: GetAdminChatListQuery) -> PaginatedAdminChatListView:
        chats = await self._chat_reader.list_admin_chats(
            limit=query.limit,
            offset=query.offset,
            status=query.status,
        )

        return PaginatedAdminChatListView(
            chats=chats.items,
            pagination=OffsetPagination.create(
                total=chats.total,
                limit=query.limit,
                offset=query.offset,
            ),
        )
