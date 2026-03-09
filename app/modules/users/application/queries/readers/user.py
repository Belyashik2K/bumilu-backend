from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
    Optional,
)
from uuid import UUID

if TYPE_CHECKING:
    from app.modules.users.application.queries.shared_views import UserInfoView


class IUserReader(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional["UserInfoView"]: ...
