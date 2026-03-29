from app.core.domain.value_objects.id import ChatIdVO
from app.core.exceptions.application.base import ApplicationNotFoundException


class ChatNotFound(ApplicationNotFoundException):
    def __init__(self, chat_id: ChatIdVO) -> None:
        super().__init__(message="Chat not found", details={"chat_id": str(chat_id)})
