from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.users.domain.models.user import User
from app.modules.users.domain.value_objects import UserEmailVO


class IUserRepository(IBaseRepository[User], ABC):
    @abstractmethod
    async def get_by_email(self, email: UserEmailVO) -> User | None: ...
