from app.core.domain.value_objects.id import ChatIdVO
from app.core.exceptions.domain.base import DomainConflictException


class ChatNotEscalatedToAdmin(DomainConflictException):
    def __init__(self, chat_id: ChatIdVO) -> None:
        super().__init__(
            message="Chat must be escalated to admin to perform this action",
            details={"chat_id": str(chat_id)},
        )
