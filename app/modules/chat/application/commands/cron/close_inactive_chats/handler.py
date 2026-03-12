from datetime import timedelta

from app.core.application.commands import (
    EmptyCommand,
    ICommandHandler,
)
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.shared.enums import ChatCloseReasonEnum


class CloseInactiveChatsCommandHandler(ICommandHandler[EmptyCommand]):
    def __init__(
        self,
        chat_repository: IChatRepository,
        transaction_manager: ITransactionManager,
        inactivity_threshold_minutes: int,
    ) -> None:
        super().__init__(transaction_manager)
        self._chat_repository = chat_repository
        self._inactivity_threshold_minutes = inactivity_threshold_minutes

    async def handle(self, command: EmptyCommand) -> None:
        now = get_current_dt()
        threshold = now - timedelta(minutes=self._inactivity_threshold_minutes)
        inactive_chats = await self._chat_repository.get_inactive_open_chats(threshold)

        for chat in inactive_chats:
            chat.close(reason=ChatCloseReasonEnum.INACTIVITY, now=now)
            await self._chat_repository.save(chat)
