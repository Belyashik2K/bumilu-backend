from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from app.core.shared.domain.value_objects.id import (
    PrincipalIdVO,
    SessionIdVO,
)
from app.core.shared.enums import UserRoleEnum
from app.modules.auth.shared.enums import PrincipalTypeEnum
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


@dataclass(frozen=True, slots=True)
class TokenInfoDTO:
    principal_id: PrincipalIdVO
    principal_type: PrincipalTypeEnum
    role: UserRoleEnum | StaffRoleEnum
    session_id: SessionIdVO
    issued_at: int
    expires_at: int


class IAccessTokenManager(ABC):
    @abstractmethod
    def issue(
        self,
        principal_id: PrincipalIdVO,
        principal_type: PrincipalTypeEnum,
        session_id: SessionIdVO,
        role: UserRoleEnum | StaffRoleEnum,
        ttl: int,
    ) -> str: ...

    @abstractmethod
    def validate_and_decode(self, token: str) -> TokenInfoDTO: ...
