from abc import (
    ABC,
    abstractmethod,
)

from app.core.shared.domain.value_objects.id import (
    SessionIdVO,
    UserIdVO,
)
from app.core.shared.enums import UserRoleEnum


class IAccessTokenManager(ABC):
    @abstractmethod
    def issue(
        self,
        user_id: UserIdVO,
        session_id: SessionIdVO,
        role: UserRoleEnum,
        ttl: int,
    ) -> str: ...

    # @abstractmethod
    # def validate(self, token: str) -> bool: ...
