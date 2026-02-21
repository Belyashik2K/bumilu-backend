import jwt

from app.core.shared.domain.value_objects.id import (
    SessionIdVO,
    UserIdVO,
)
from app.core.shared.enums import UserRoleEnum
from app.core.shared.utils import get_current_dt
from app.modules.auth.application.interfaces.managers.access_token import (
    IAccessTokenManager,
)


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

    def issue(
        self,
        user_id: UserIdVO,
        session_id: SessionIdVO,
        role: UserRoleEnum,
        ttl: int,
    ) -> str:
        payload = {
            "type": "access",
            "sub": user_id.value,
            "iss": self._issuer,
            "exp": ttl,
            "iat": get_current_dt(),
            "session_id": session_id.value,
            "role": role.value,
        }
        token = jwt.encode(
            payload=payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )
        return token
