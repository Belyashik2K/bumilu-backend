import pytest
from app.modules.auth.application.commands.staff.login.handler import (
    LoginAsStaffMemberCommandHandler,
)
from app.modules.auth.application.commands.user.email.verify_code.handler import (
    VerifyEmailCodeAtLoginCommandHandler,
)

from tests.unit.application.auth.fakes import (
    FakeAuthSessionRepository,
    FakeAuthSessionService,
    FakeDeviceRepository,
    FakeEmailLoginChallengeStore,
    FakePrincipalRepository,
    FakeStaffMemberRepository,
    FakeStaffPasswordHasher,
    FakeTransactionManager,
    FakeUserRepository,
    FakeVerificationCodeHasher,
)


@pytest.fixture
def transaction_manager() -> FakeTransactionManager:
    return FakeTransactionManager()


@pytest.fixture
def principal_repository() -> FakePrincipalRepository:
    return FakePrincipalRepository()


@pytest.fixture
def staff_member_repository() -> FakeStaffMemberRepository:
    return FakeStaffMemberRepository()


@pytest.fixture
def staff_password_hasher() -> FakeStaffPasswordHasher:
    return FakeStaffPasswordHasher()


@pytest.fixture
def user_repository() -> FakeUserRepository:
    return FakeUserRepository()


@pytest.fixture
def device_repository() -> FakeDeviceRepository:
    return FakeDeviceRepository()


@pytest.fixture
def auth_session_repository() -> FakeAuthSessionRepository:
    return FakeAuthSessionRepository()


@pytest.fixture
def challenge_store() -> FakeEmailLoginChallengeStore:
    return FakeEmailLoginChallengeStore(consume_result=True)


@pytest.fixture
def code_hasher() -> FakeVerificationCodeHasher:
    return FakeVerificationCodeHasher()


@pytest.fixture
def auth_session_service() -> FakeAuthSessionService:
    return FakeAuthSessionService()


@pytest.fixture
def login_as_staff_member_handler(
    transaction_manager: FakeTransactionManager,
    principal_repository: FakePrincipalRepository,
    staff_member_repository: FakeStaffMemberRepository,
    staff_password_hasher: FakeStaffPasswordHasher,
    auth_session_service: FakeAuthSessionService,
) -> LoginAsStaffMemberCommandHandler:
    return LoginAsStaffMemberCommandHandler(
        transaction_manager=transaction_manager,
        principal_repository=principal_repository,
        staff_member_repository=staff_member_repository,
        staff_password_hasher=staff_password_hasher,
        auth_session_service=auth_session_service,
    )


@pytest.fixture
def verify_email_code_at_login_handler(
    user_repository: FakeUserRepository,
    device_repository: FakeDeviceRepository,
    principal_repository: FakePrincipalRepository,
    auth_session_repository: FakeAuthSessionRepository,
    auth_session_service: FakeAuthSessionService,
    challenge_store: FakeEmailLoginChallengeStore,
    code_hasher: FakeVerificationCodeHasher,
    transaction_manager: FakeTransactionManager,
) -> VerifyEmailCodeAtLoginCommandHandler:
    return VerifyEmailCodeAtLoginCommandHandler(
        user_repository=user_repository,
        device_repository=device_repository,
        principal_repository=principal_repository,
        auth_session_repository=auth_session_repository,
        auth_session_service=auth_session_service,
        challenge_store=challenge_store,
        code_hasher=code_hasher,
        transaction_manager=transaction_manager,
    )
