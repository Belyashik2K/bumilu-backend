from dishka import (
    Provider,
    Scope,
    provide,
)
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.interfaces.transaction_manager import (
    ITransactionManager,
)
from app.core.infrastructure.config import AppConfig
from app.modules.auth.application.commands.logout import LogoutCommandHandler
from app.modules.auth.application.commands.user.email import (
    RequestEmailCodeAtLoginCommandHandler,
    VerifyEmailCodeAtLoginCommandHandler,
)
from app.modules.auth.application.commands.user.guest import LoginAsGuestCommandHandler
from app.modules.auth.application.commands.user.refresh_session import (
    RefreshAuthSessionCommandHandler,
)
from app.modules.auth.application.interfaces.email_sender import IEmailSender
from app.modules.auth.application.interfaces.generators import (
    IRefreshTokenGenerator,
    IVerificationCodeGenerator,
)
from app.modules.auth.application.interfaces.hashers import (
    ITokenHasher,
    IVerificationCodeHasher,
)
from app.modules.auth.application.interfaces.managers.access_token import (
    IAccessTokenManager,
)
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.application.interfaces.repositories.device import (
    IDeviceRepository,
)
from app.modules.auth.application.interfaces.repositories.principal import (
    IPrincipalRepository,
)
from app.modules.auth.application.interfaces.stores.email_login import (
    IEmailLoginChallengeStore,
)
from app.modules.auth.application.services.auth_session import AuthSessionService
from app.modules.auth.infrastructure.database.repositories.auth_session import (
    SQLAlchemyAuthSessionRepository,
)
from app.modules.auth.infrastructure.database.repositories.device import (
    SQLAlchemyDeviceRepository,
)
from app.modules.auth.infrastructure.database.repositories.principal import (
    SQLAlchemyPrincipalRepository,
)
from app.modules.auth.infrastructure.generators.secrets_refresh_token_generator import (
    SecretsRefreshTokenGenerator,
)
from app.modules.auth.infrastructure.generators.secrets_verification_code_generator import (
    SecretsVerificationCodeGenerator,
)
from app.modules.auth.infrastructure.hashers.hmac_token_hasher import HMACTokenHasher
from app.modules.auth.infrastructure.hashers.hmac_verification_code_hasher import (
    HMACVerificationCodeHasher,
)
from app.modules.auth.infrastructure.managers.pyjwt_access_token_manager import (
    PyJWTAccessTokenManager,
)
from app.modules.auth.infrastructure.smtplib_email_sender import SMTPLibEmailSender
from app.modules.auth.infrastructure.stores.redis_email_challenge_store import (
    RedisEmailLoginChallengeStore,
)
from app.modules.users.application.interfaces.repositories.user import IUserRepository


class AuthProvider(Provider):
    @provide(scope=Scope.APP, provides=IAccessTokenManager)
    async def access_token_manager(
        self,
        config: AppConfig,
    ) -> PyJWTAccessTokenManager:
        return PyJWTAccessTokenManager(
            secret_key=config.auth.session.tokens.access.secret_key,
            algorithm=config.auth.session.tokens.access.algorithm,
            issuer=config.auth.session.tokens.access.issuer,
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
            secret=config.auth.session.tokens.refresh.hash_secret_key
        )

    @provide(scope=Scope.APP, provides=IVerificationCodeHasher)
    async def verification_code_hasher(
        self,
        config: AppConfig,
    ) -> HMACVerificationCodeHasher:
        return HMACVerificationCodeHasher(secret=config.auth.otp.hash_secret_key)

    @provide(scope=Scope.APP, provides=IVerificationCodeGenerator)
    async def verification_code_generator(
        self,
        config: AppConfig,
    ) -> SecretsVerificationCodeGenerator:
        return SecretsVerificationCodeGenerator(
            code_length=config.auth.otp.length,
        )

    @provide(scope=Scope.APP, provides=IEmailSender)
    async def email_sender(
        self,
        config: AppConfig,
    ) -> IEmailSender:
        return SMTPLibEmailSender(
            host=config.auth.email.smtp.host,
            port=config.auth.email.smtp.port,
            login=config.auth.email.smtp.username,
            password=config.auth.email.smtp.password,
            from_author=config.auth.email.smtp.from_name,
            from_email=config.auth.email.smtp.from_email,
            timeout=config.auth.email.smtp.timeout,
        )

    @provide(scope=Scope.APP, provides=IEmailLoginChallengeStore)
    async def email_login_challenge_store(
        self, config: AppConfig, redis: Redis
    ) -> RedisEmailLoginChallengeStore:
        return RedisEmailLoginChallengeStore(
            redis=redis,
            key_prefix=config.auth.otp.storage_key_prefix,
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

    @provide(scope=Scope.REQUEST, provides=IPrincipalRepository)
    async def principal_repository(
        self, session: AsyncSession
    ) -> SQLAlchemyPrincipalRepository:
        return SQLAlchemyPrincipalRepository(
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
            access_ttl_seconds=config.auth.session.tokens.access.ttl_sec,
            refresh_ttl_seconds=config.auth.session.tokens.refresh.ttl_sec,
            auth_session_repository=auth_session_repository,
            access_token_manager=access_token_manager,
            refresh_token_generator=refresh_token_generator,
            token_hasher=token_hasher,
        )

    @provide(scope=Scope.REQUEST)
    async def login_as_guest_handler(
        self,
        user_repository: IUserRepository,
        device_repository: IDeviceRepository,
        principal_repository: IPrincipalRepository,
        auth_service_repository: IAuthSessionRepository,
        auth_session_service: AuthSessionService,
        transaction_manager: ITransactionManager,
    ) -> LoginAsGuestCommandHandler:
        return LoginAsGuestCommandHandler(
            transaction_manager=transaction_manager,
            user_repository=user_repository,
            device_repository=device_repository,
            principal_repository=principal_repository,
            auth_session_repository=auth_service_repository,
            auth_session_service=auth_session_service,
        )

    @provide(scope=Scope.REQUEST)
    async def refresh_session_handler(
        self,
        auth_session_repository: IAuthSessionRepository,
        user_repository: IUserRepository,
        auth_session_service: AuthSessionService,
        transaction_manager: ITransactionManager,
    ) -> RefreshAuthSessionCommandHandler:
        return RefreshAuthSessionCommandHandler(
            transaction_manager=transaction_manager,
            auth_session_repository=auth_session_repository,
            user_repository=user_repository,
            auth_session_service=auth_session_service,
        )

    @provide(scope=Scope.REQUEST)
    async def logout_uc(
        self,
        auth_session_repository: IAuthSessionRepository,
        auth_session_service: AuthSessionService,
        transaction_manager: ITransactionManager,
    ) -> LogoutCommandHandler:
        return LogoutCommandHandler(
            transaction_manager=transaction_manager,
            auth_session_repository=auth_session_repository,
            auth_session_service=auth_session_service,
        )

    @provide(scope=Scope.REQUEST)
    async def request_email_code_at_login_handler(
        self,
        config: AppConfig,
        code_generator: IVerificationCodeGenerator,
        code_hasher: IVerificationCodeHasher,
        challenge_store: IEmailLoginChallengeStore,
        email_sender: IEmailSender,
        transaction_manager: ITransactionManager,
    ) -> RequestEmailCodeAtLoginCommandHandler:
        return RequestEmailCodeAtLoginCommandHandler(
            transaction_manager=transaction_manager,
            code_generator=code_generator,
            code_hasher=code_hasher,
            challenge_store=challenge_store,
            email_sender=email_sender,
            email_subject=config.auth.email.templates.otp.subject,
            email_body_template=config.auth.email.templates.otp.body,
            resend_cooldown_seconds=config.auth.otp.resend_cooldown_sec,
            ttl_seconds=config.auth.otp.ttl_min * 60,
        )

    @provide(scope=Scope.REQUEST)
    async def verify_email_code_at_login_handler(
        self,
        auth_session_repository: IAuthSessionRepository,
        user_repository: IUserRepository,
        device_repository: IDeviceRepository,
        principal_repository: IPrincipalRepository,
        auth_session_service: AuthSessionService,
        challenge_store: IEmailLoginChallengeStore,
        code_hasher: IVerificationCodeHasher,
        transaction_manager: ITransactionManager,
    ) -> VerifyEmailCodeAtLoginCommandHandler:
        return VerifyEmailCodeAtLoginCommandHandler(
            transaction_manager=transaction_manager,
            auth_session_repository=auth_session_repository,
            user_repository=user_repository,
            device_repository=device_repository,
            principal_repository=principal_repository,
            auth_session_service=auth_session_service,
            challenge_store=challenge_store,
            code_hasher=code_hasher,
        )
