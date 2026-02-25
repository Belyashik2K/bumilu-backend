from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from app.core.shared.domain.value_objects.id import (
    SessionIdVO,
    UserIdVO,
)
from app.core.shared.enums import UserRoleEnum


@dataclass(frozen=True, slots=True)
class TokenInfoDTO:
    user_id: UserIdVO
    session_id: SessionIdVO
    role: UserRoleEnum
    issued_at: int
    expires_at: int


class IAccessTokenManager(ABC):
    @abstractmethod
    def issue(
        self,
        user_id: UserIdVO,
        session_id: SessionIdVO,
        role: UserRoleEnum,
        ttl: int,
    ) -> str: ...

    @abstractmethod
    def validate_and_decode(self, token: str) -> TokenInfoDTO: ...
