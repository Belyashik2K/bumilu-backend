from abc import ABC

from mypy.metastore import abstractmethod

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.chat.domain.models.chat import Chat


class IChatRepository(IBaseRepository[Chat], ABC):
    @abstractmethod
    async def get_active_chat_by_user_id(self, user_id: UserIdVO) -> Chat | None: ...
