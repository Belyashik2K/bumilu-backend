from datetime import (
    datetime,
    timedelta,
)

import jwt

from app.core.domain.value_objects.id import (
    PrincipalIdVO,
    SessionIdVO,
)
from app.core.enums import UserRoleEnum
from app.core.utils import get_current_dt
from app.modules.auth.application.interfaces.managers.access_token import (
    IAccessTokenManager,
    TokenInfoDTO,
)
from app.modules.auth.shared.enums import PrincipalTypeEnum
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


class PyJWTAccessTokenManager(IAccessTokenManager):
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        issuer: str,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._issuer = issuer

    @staticmethod
    def _get_expiration_time(seconds: int) -> datetime:
        return get_current_dt() + timedelta(seconds=seconds)

    def issue(
        self,
        principal_id: PrincipalIdVO,
        principal_type: PrincipalTypeEnum,
        session_id: SessionIdVO,
        role: UserRoleEnum,
        ttl: int,
    ) -> str:
        payload = {
            "type": "access",
            "sub": str(principal_id),
            "principal_type": principal_type.value,
            "iss": self._issuer,
            "exp": self._get_expiration_time(seconds=ttl),
            "iat": get_current_dt(),
            "session_id": str(session_id),
            "role": role.value,
        }
        token = jwt.encode(
            payload=payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )
        return token

    def validate_and_decode(self, token: str) -> TokenInfoDTO:
        try:
            payload = jwt.decode(
                jwt=token,
                key=self._secret_key,
                algorithms=[self._algorithm],
                issuer=self._issuer,
            )
        except jwt.PyJWTError as e:
            raise ValueError("Invalid token") from e

        if payload.get("type") != "access":
            raise ValueError("Invalid token type")

        principal_type = PrincipalTypeEnum(payload["principal_type"])
        role = payload["role"]

        mapped_role = {
            PrincipalTypeEnum.USER: lambda: UserRoleEnum(role),
            PrincipalTypeEnum.STAFF: lambda: StaffRoleEnum(role),
        }

        return TokenInfoDTO(
            principal_type=principal_type,
            principal_id=PrincipalIdVO.from_str(payload["sub"]),
            session_id=SessionIdVO.from_str(payload["session_id"]),
            role=mapped_role[principal_type](),
            issued_at=payload["iat"],
            expires_at=payload["exp"],
        )
