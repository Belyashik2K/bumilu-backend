from app.core.application.use_cases.base import (
    IBaseUseCase,
)
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.queries.user.get_info import (
    GetUserActiveChatInfoInputDTO,
    GetUserActiveChatInfoOutputDTO,
)
from app.modules.chat.application.shared.dtos import ChatInfoDTO


class GetUserActiveChatInfoUseCase(
    IBaseUseCase[GetUserActiveChatInfoInputDTO, GetUserActiveChatInfoOutputDTO]
):
    def __init__(
        self,
        chat_repository: IChatRepository,
    ) -> None:
        self._chat_repository = chat_repository

    async def execute(
        self, input_data: GetUserActiveChatInfoInputDTO
    ) -> GetUserActiveChatInfoOutputDTO:
        user_id = UserIdVO.from_uuid(input_data.user_id)
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

        return GetUserActiveChatInfoOutputDTO(active_chat=active_chat_dto)
