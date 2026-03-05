from abc import ABC

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.chat.domain.models.chat_message import ChatMessage


class IChatMessageRepository(IBaseRepository[ChatMessage], ABC): ...
