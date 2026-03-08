from app.core.application.queries import IQueryHandler
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.queries.user.get_info import (
    GetUserActiveChatInfoQuery,
    GetUserActiveChatInfoQueryResult,
)
from app.modules.chat.application.shared.dtos import ChatInfoDTO


class GetUserActiveChatInfoQueryHandler(
    IQueryHandler[GetUserActiveChatInfoQuery, GetUserActiveChatInfoQueryResult]
):
    def __init__(
        self,
        chat_repository: IChatRepository,
    ) -> None:
        self._chat_repository = chat_repository

    async def handle(
        self, query: GetUserActiveChatInfoQuery
    ) -> GetUserActiveChatInfoQueryResult:
        user_id = UserIdVO.from_uuid(query.user_id)
        active_chat = await self._chat_repository.find_active_chat(user_id)

        active_chat_dto = (
            ChatInfoDTO(
                id=active_chat.id.value,
                user_id=active_chat.user_id.value,
                language=active_chat.language,
                status=active_chat.status,
                last_activity_at=active_chat.last_activity_at,
            )
            if active_chat
            else None
        )

        return GetUserActiveChatInfoQueryResult(active_chat=active_chat_dto)
