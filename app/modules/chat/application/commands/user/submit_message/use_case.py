from app.core.application.use_cases.base import (
    IBaseUseCase,
)
from app.core.shared.domain.value_objects.id import UserIdVO
from app.core.shared.enums import LanguageEnum
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.commands.user.submit_message import (
    SubmitUserMessageInputDTO,
    SubmitUserMessageOutputDTO,
)
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.chat.domain.models.chat import Chat
from app.modules.chat.domain.value_objects.location import LocationVO
from app.modules.chat.domain.value_objects.message_text import MessageTextVO
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.queries.get.exceptions import UserNotFound


class SubmitUserMessageUseCase(
    IBaseUseCase[SubmitUserMessageInputDTO, SubmitUserMessageOutputDTO]
):
    def __init__(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
        user_repository: IUserRepository,
    ) -> None:
        self._chat_repository = chat_repository
        self._chat_message_repository = chat_message_repository
        self._user_repository = user_repository

    async def execute(
        self, input_data: SubmitUserMessageInputDTO
    ) -> SubmitUserMessageOutputDTO:
        user_id = UserIdVO.from_uuid(input_data.user_id)
        chat = await self._chat_repository.find_active_chat(user_id)
        now = get_current_dt()

        location: LocationVO | None = None
        if input_data.longitude and input_data.latitude:
            location = LocationVO.from_coordinates(
                latitude=input_data.latitude,
                longitude=input_data.longitude,
            )

        if not chat:
            user = await self._user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFound(user_id=user_id)

            language = LanguageEnum.EN  # TODO: Get user's preferred language

            chat = Chat.create(
                user_id=user_id,
                language=language,
                location=location,
                now=now,
            )

        message = chat.reply_as_user(
            text=MessageTextVO(input_data.text),
            location=location,
            now=now,
        )
        await self._chat_repository.save(chat)
        await self._chat_message_repository.save(message)

        return SubmitUserMessageOutputDTO(
            chat_id=chat.id.value,
            message_id=message.id.value,
        )
