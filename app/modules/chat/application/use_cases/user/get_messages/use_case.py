from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.chat.application.use_cases.shared.dtos import ChatMessageInfoDTO
from app.modules.chat.application.use_cases.user.get_messages import (
    GetUserActiveChatMessagesInputDTO,
    GetUserActiveChatMessagesOutputDTO,
)


class GetUserActiveChatMessagesUseCase(
    IBaseUseCase[
        GetUserActiveChatMessagesInputDTO,
        GetUserActiveChatMessagesOutputDTO,
    ]
):
    def __init__(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
    ) -> None:
        self._chat_repository = chat_repository
        self._chat_message_repository = chat_message_repository

    async def execute(
        self, input_data: GetUserActiveChatMessagesInputDTO
    ) -> GetUserActiveChatMessagesOutputDTO:
        user_id = UserIdVO.from_uuid(input_data.user_id)
        chat_id = await self._chat_repository.get_active_chat_id(user_id)
        if not chat_id:
            return GetUserActiveChatMessagesOutputDTO()

        messages = await self._chat_message_repository.get_chat_messages(chat_id)
        return GetUserActiveChatMessagesOutputDTO(
            chat_id=chat_id.value,
            messages=[
                ChatMessageInfoDTO(
                    id=message.id.value,
                    author_id=message.author_id.value if message.author_id else None,
                    author_type=message.author_type,
                    text=message.text.value,
                    latitude=message.location.latitude if message.location else None,
                    longitude=message.location.longitude if message.location else None,
                )
                for message in messages
            ],
        )
