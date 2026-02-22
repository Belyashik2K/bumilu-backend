from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.config import AppConfig
from app.modules.auth.application.interfaces.managers.access_token import (
    IAccessTokenManager,
)
from app.modules.auth.application.interfaces.refresh_token_generator import (
    IRefreshTokenGenerator,
)
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.application.interfaces.repositories.device import (
    IDeviceRepository,
)
from app.modules.auth.application.interfaces.token_hasher import ITokenHasher
from app.modules.auth.application.services.auth_session import AuthSessionService
from app.modules.auth.application.use_cases.guest.login import LoginAsGuestUseCase
from app.modules.auth.application.use_cases.logout.use_case import LogoutUseCase
from app.modules.auth.application.use_cases.refresh_session.use_case import (
    RefreshAuthSessionUseCase,
)
from app.modules.auth.infrastructure.auth.access import (
    PyJWTAccessTokenManager,
)
from app.modules.auth.infrastructure.auth.hashing import (
    HMACTokenHasher,
)
from app.modules.auth.infrastructure.auth.refresh import (
    SecretsRefreshTokenGenerator,
)
from app.modules.auth.infrastructure.database.repositories.auth_session import (
    SQLAlchemyAuthSessionRepository,
)
from app.modules.auth.infrastructure.database.repositories.device import (
    SQLAlchemyDeviceRepository,
)
from app.modules.users.application.interfaces.repositories.user import IUserRepository


class AuthProvider(Provider):
    @provide(scope=Scope.APP, provides=IAccessTokenManager)
    async def access_token_manager(
        self,
        config: AppConfig,
    ) -> PyJWTAccessTokenManager:
        return PyJWTAccessTokenManager(
            secret_key=config.jwt.secret_key,
            algorithm=config.jwt.algorithm,
            issuer=config.jwt.issuer,
        )

    @provide(scope=Scope.APP, provides=IRefreshTokenGenerator)
    async def refresh_token_generator(self) -> SecretsRefreshTokenGenerator:
        return SecretsRefreshTokenGenerator()

    @provide(scope=Scope.APP, provides=ITokenHasher)
    async def token_hasher(
        self,
        config: AppConfig,
    ) -> HMACTokenHasher:
        return HMACTokenHasher(
            secret=config.hmac.secret_key,
        )

    @provide(scope=Scope.REQUEST, provides=IAuthSessionRepository)
    async def auth_session_repository(
        self, session: AsyncSession
    ) -> SQLAlchemyAuthSessionRepository:
        return SQLAlchemyAuthSessionRepository(
            session=session,
        )

    @provide(scope=Scope.REQUEST, provides=IDeviceRepository)
    async def device_repository(
        self, session: AsyncSession
    ) -> SQLAlchemyDeviceRepository:
        return SQLAlchemyDeviceRepository(
            session=session,
        )

    @provide(scope=Scope.REQUEST)
    async def auth_session_service(
        self,
        config: AppConfig,
        auth_session_repository: IAuthSessionRepository,
        access_token_manager: IAccessTokenManager,
        refresh_token_generator: IRefreshTokenGenerator,
        token_hasher: ITokenHasher,
    ) -> AuthSessionService:
        return AuthSessionService(
            access_ttl_seconds=config.jwt.access_token_ttl_sec,
            refresh_ttl_seconds=config.jwt.refresh_token_ttl_sec,
            auth_session_repository=auth_session_repository,
            access_token_manager=access_token_manager,
            refresh_token_generator=refresh_token_generator,
            token_hasher=token_hasher,
        )

    @provide(scope=Scope.REQUEST)
    async def login_as_guest_uc(
        self,
        user_repository: IUserRepository,
        device_repository: IDeviceRepository,
        auth_service_repository: IAuthSessionRepository,
        auth_session_service: AuthSessionService,
    ) -> LoginAsGuestUseCase:
        return LoginAsGuestUseCase(
            user_repository=user_repository,
            device_repository=device_repository,
            auth_session_repository=auth_service_repository,
            auth_session_service=auth_session_service,
        )

    @provide(scope=Scope.REQUEST)
    async def refresh_session_uc(
        self,
        auth_session_repository: IAuthSessionRepository,
        user_repository: IUserRepository,
        auth_session_service: AuthSessionService,
    ) -> RefreshAuthSessionUseCase:
        return RefreshAuthSessionUseCase(
            auth_session_repository=auth_session_repository,
            user_repository=user_repository,
            auth_session_service=auth_session_service,
        )

    @provide(scope=Scope.REQUEST)
    async def logout_uc(
        self,
        auth_session_repository: IAuthSessionRepository,
        auth_session_service: AuthSessionService,
    ) -> LogoutUseCase:
        return LogoutUseCase(
            auth_session_repository=auth_session_repository,
            auth_session_service=auth_session_service,
        )
