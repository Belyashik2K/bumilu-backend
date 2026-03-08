from app.core.shared.domain.value_objects.id import ChatIdVO
from app.core.shared.exceptions.application.base import ApplicationNotFoundException


class ChatNotFound(ApplicationNotFoundException):
    def __init__(self, chat_id: ChatIdVO) -> None:
        super().__init__(message="Chat not found", details={"chat_id": str(chat_id)})
