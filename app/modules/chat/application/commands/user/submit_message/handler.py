from app.core.application.commands import ICommandHandlerWithResult
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.shared.domain.value_objects.id import PrincipalIdVO
from app.core.shared.enums import LanguageEnum
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.commands.user.submit_message import (
    SubmitUserMessageCommand,
    SubmitUserMessageCommandResult,
)
from app.modules.chat.application.interfaces.chat_reply_dispatcher import (
    IChatReplyDispatcher,
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


class SubmitUserMessageCommandHandler(
    ICommandHandlerWithResult[SubmitUserMessageCommand, SubmitUserMessageCommandResult]
):
    def __init__(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
        user_repository: IUserRepository,
        chat_reply_dispatcher: IChatReplyDispatcher,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._chat_repository = chat_repository
        self._chat_message_repository = chat_message_repository
        self._user_repository = user_repository
        self._chat_reply_dispatcher = chat_reply_dispatcher

    async def handle(
        self, command: SubmitUserMessageCommand
    ) -> SubmitUserMessageCommandResult:
        user_id = PrincipalIdVO.from_uuid(command.user_id)
        chat = await self._chat_repository.find_active_chat(user_id)
        now = get_current_dt()

        location: LocationVO | None = None
        if command.longitude and command.latitude:
            location = LocationVO.from_coordinates(
                latitude=command.latitude,
                longitude=command.longitude,
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
            text=MessageTextVO(command.text),
            location=location,
            now=now,
        )
        await self._chat_repository.save(chat)
        await self._chat_message_repository.save(message)

        await self._chat_reply_dispatcher.dispatch(
            chat_id=chat.id.value, delay_seconds=5
        )

        return SubmitUserMessageCommandResult(
            chat_id=chat.id.value,
            message_id=message.id.value,
        )
