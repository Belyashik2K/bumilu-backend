import logging
from dataclasses import (
    dataclass,
)
from datetime import timedelta

from app.core.shared.domain.value_objects.id import (
    DeviceIdVO,
    UserIdVO,
)
from app.core.shared.enums import UserRoleEnum
from app.core.shared.utils import (
    get_current_dt,
    prepare_extras,
)
from app.modules.auth.application.interfaces.generators import (
    IRefreshTokenGenerator,
)
from app.modules.auth.application.interfaces.hashers import ITokenHasher
from app.modules.auth.application.interfaces.managers.access_token import (
    IAccessTokenManager,
)
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.domain.models.auth_session import AuthSession

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class IssuedAuthTokens:
    access_token: str
    refresh_token: str
    access_expires_in: int
    refresh_expires_in: int


@dataclass(frozen=True, slots=True)
class AccessClaims:
    user_id: str
    session_id: str
    role: UserRoleEnum


@dataclass(frozen=True, slots=True)
class SessionContext:
    user_id: str
    session_id: str
    device_id: str
    role: UserRoleEnum


class AuthSessionService:
    def __init__(
        self,
        access_ttl_seconds: int,
        refresh_ttl_seconds: int,
        auth_session_repository: IAuthSessionRepository,
        access_token_manager: IAccessTokenManager,
        refresh_token_generator: IRefreshTokenGenerator,
        token_hasher: ITokenHasher,
    ) -> None:
        self._access_ttl_seconds = access_ttl_seconds
        self._refresh_ttl_seconds = refresh_ttl_seconds

        self._auth_session_repository = auth_session_repository
        self._access_token_manager = access_token_manager
        self._refresh_token_generator = refresh_token_generator
        self._token_hasher = token_hasher

    def get_token_hash(self, token: str) -> str:
        return self._token_hasher.hash(token)

    async def issue(
        self,
        *,
        user_id: UserIdVO,
        device_id: DeviceIdVO,
        role: UserRoleEnum,
    ) -> IssuedAuthTokens:
        token = self._refresh_token_generator.generate()
        token_hash = self.get_token_hash(token)

        session = AuthSession.create(
            user_id=user_id,
            refresh_token_hash=token_hash,
            device_id=device_id,
            expires_at=get_current_dt() + timedelta(seconds=self._refresh_ttl_seconds),
        )
        await self._auth_session_repository.save(session)

        access_token = self._access_token_manager.issue(
            user_id=user_id,
            session_id=session.id,
            role=role,
            ttl=self._access_ttl_seconds,
        )

        logger.info(
            "auth_session_issued",
            extra=prepare_extras(
                user_id=str(user_id),
                device_id=str(device_id),
                session_id=str(session.id),
                access_ttl_s=self._access_ttl_seconds,
                refresh_ttl_s=self._refresh_ttl_seconds,
            ),
        )

        return IssuedAuthTokens(
            access_token=access_token,
            refresh_token=token,
            access_expires_in=self._access_ttl_seconds,
            refresh_expires_in=self._refresh_ttl_seconds,
        )

    async def rotate(
        self,
        *,
        session: AuthSession,
        role: UserRoleEnum,
    ) -> IssuedAuthTokens:
        new_refresh_token = self._refresh_token_generator.generate()
        new_refresh_token_hash = self.get_token_hash(new_refresh_token)

        session.rotate(new_refresh_token_hash)  # TODO: extend expiration time
        await self._auth_session_repository.save(session)

        access_token = self._access_token_manager.issue(
            user_id=session.user_id,
            session_id=session.id,
            role=role,
            ttl=self._access_ttl_seconds,
        )

        logger.info(
            "auth_session_rotated",
            extra=prepare_extras(
                user_id=str(session.user_id),
                device_id=str(session.device_id),
                session_id=str(session.id),
            ),
        )

        return IssuedAuthTokens(
            access_token=access_token,
            refresh_token=new_refresh_token,
            access_expires_in=self._access_ttl_seconds,
            refresh_expires_in=self._refresh_ttl_seconds,
        )

    async def revoke(self, session: AuthSession) -> None:
        session.revoke()

        logger.info(
            "auth_session_revoked",
            extra=prepare_extras(
                user_id=str(session.user_id),
                device_id=str(session.device_id),
                session_id=str(session.id),
            ),
        )

        await self._auth_session_repository.save(session)
