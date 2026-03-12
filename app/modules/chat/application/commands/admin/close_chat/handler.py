from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.shared.domain.value_objects.id import ChatIdVO
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.commands.admin.close_chat.command import (
    CloseChatAsAdminCommand,
)
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.shared.exceptions import ChatNotFound
from app.modules.chat.shared.enums import ChatCloseReasonEnum


class CloseChatAsAdminCommandHandler(ICommandHandler[CloseChatAsAdminCommand]):
    def __init__(
        self,
        chat_repository: IChatRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._chat_repository = chat_repository

    async def handle(self, command: CloseChatAsAdminCommand) -> None:
        now = get_current_dt()
        chat_id = ChatIdVO.from_uuid(command.chat_id)

        chat = await self._chat_repository.get_by_id(chat_id)
        if chat is None:
            raise ChatNotFound(chat_id=chat_id)

        chat.close(reason=ChatCloseReasonEnum.BY_ADMIN, now=now)
        await self._chat_repository.save(chat)
