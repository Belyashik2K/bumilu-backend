from app.core.shared.domain.value_objects.id import ChatIdVO
from app.core.shared.exceptions.domain.base import DomainConflictException


class ChatNotEscalatedToAdmin(DomainConflictException):
    def __init__(self, chat_id: ChatIdVO) -> None:
        super().__init__(
            message="Chat must be escalated to admin to reply as admin",
            details={"chat_id": chat_id},
        )
