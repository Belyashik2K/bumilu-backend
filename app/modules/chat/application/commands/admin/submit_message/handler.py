from app.core.application.commands import ICommandHandlerWithResult
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.shared.domain.value_objects.id import (
    ChatIdVO,
    PrincipalIdVO,
)
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.commands.admin.submit_message import (
    SubmitAdminMessageCommand,
    SubmitAdminMessageCommandResult,
)
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.chat.application.shared.exceptions import ChatNotFound
from app.modules.chat.domain.value_objects.message_text import MessageTextVO


class SubmitAdminMessageCommandHandler(
    ICommandHandlerWithResult[
        SubmitAdminMessageCommand, SubmitAdminMessageCommandResult
    ]
):
    def __init__(
        self,
        chat_repository: IChatRepository,
        chat_message_repository: IChatMessageRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._chat_repository = chat_repository
        self._chat_message_repository = chat_message_repository

    async def handle(
        self,
        command: SubmitAdminMessageCommand,
    ) -> SubmitAdminMessageCommandResult:
        author_id = PrincipalIdVO.from_uuid(command.actor_id)
        chat_id = ChatIdVO.from_uuid(command.chat_id)
        text = MessageTextVO(command.text)
        now = get_current_dt()

        chat = await self._chat_repository.get_by_id(chat_id)
        if not chat:
            raise ChatNotFound(chat_id=chat_id)

        # We believe that only admins can call this use case,
        # but later we might want to add a check here to ensure that the actor is indeed an admin.
        message = chat.reply_as_admin(author_id=author_id, text=text, now=now)

        await self._chat_repository.save(chat)
        await self._chat_message_repository.save(message)

        return SubmitAdminMessageCommandResult(
            message_id=message.id.value,
        )
