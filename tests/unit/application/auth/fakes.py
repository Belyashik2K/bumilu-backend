from typing import Any

from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import DeviceIdVO, IdVO
from app.modules.auth.application.interfaces.hashers.staff_password import (
    IStaffPasswordHasher,
)
from app.modules.auth.application.interfaces.hashers.verification_code import (
    IVerificationCodeHasher,
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
from app.modules.auth.application.services.auth_session import (
    AuthSessionService,
    IssuedAuthTokens,
)
from app.modules.auth.domain.models.auth_session import AuthSession
from app.modules.auth.domain.models.device import Device
from app.modules.auth.domain.models.principal import Principal
from app.modules.staff.application.interfaces.repositories.staff_member import (
    IStaffMemberRepository,
)
from app.modules.staff.domain.models.staff_member import StaffMember
from app.modules.staff.domain.value_objects.staff_email import StaffMemberEmailVO
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.domain.models.user import User
from app.modules.users.domain.value_objects import UserEmailVO


class FakeTransactionManager(ITransactionManager):
    async def __aenter__(self) -> "FakeTransactionManager":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        return None


class FakePrincipalRepository(IPrincipalRepository):
    def __init__(self) -> None:
        self.store: dict[str, Principal] = {}

    async def save(self, entity: Principal) -> Principal:
        self.store[str(entity.id)] = entity
        return entity

    async def batch_save(self, entities: list[Principal]) -> list[Principal]:
        for entity in entities:
            await self.save(entity)
        return entities

    async def get_by_id(self, _id: IdVO) -> Principal | None:
        return self.store.get(str(_id))


class FakeStaffMemberRepository(IStaffMemberRepository):
    def __init__(self) -> None:
        self.store: dict[str, StaffMember] = {}

    async def save(self, entity: StaffMember) -> StaffMember:
        self.store[str(entity.id)] = entity
        return entity

    async def batch_save(self, entities: list[StaffMember]) -> list[StaffMember]:
        for entity in entities:
            await self.save(entity)
        return entities

    async def get_by_id(self, _id: IdVO) -> StaffMember | None:
        return self.store.get(str(_id))

    async def get_by_email(self, email: StaffMemberEmailVO) -> StaffMember | None:
        return next(
            (m for m in self.store.values() if m.email.value == email.value),
            None,
        )

    async def total_staff_members(self) -> int:
        return len(self.store)


class FakeStaffPasswordHasher(IStaffPasswordHasher):
    def hash(self, password: str) -> str:
        return f"hashed::{password}"

    def verify(self, password: str, password_hash: str) -> bool:
        return password_hash == self.hash(password)


class FakeUserRepository(IUserRepository):
    def __init__(self) -> None:
        self.store: dict[str, User] = {}

    async def save(self, entity: User) -> User:
        self.store[str(entity.id)] = entity
        return entity

    async def batch_save(self, entities: list[User]) -> list[User]:
        for entity in entities:
            await self.save(entity)
        return entities

    async def get_by_id(self, _id: IdVO) -> User | None:
        return self.store.get(str(_id))

    async def get_by_email(self, email: UserEmailVO) -> User | None:
        return next(
            (u for u in self.store.values() if u.email == email),
            None,
        )


class FakeDeviceRepository(IDeviceRepository):
    def __init__(self) -> None:
        self.store: dict[str, Device] = {}

    async def save(self, entity: Device) -> Device:
        self.store[str(entity.id)] = entity
        return entity

    async def batch_save(self, entities: list[Device]) -> list[Device]:
        for entity in entities:
            await self.save(entity)
        return entities

    async def get_by_id(self, _id: IdVO) -> Device | None:
        return self.store.get(str(_id))


class FakeAuthSessionRepository(IAuthSessionRepository):
    def __init__(self) -> None:
        self.store: dict[str, AuthSession] = {}
        self.revoked_for_devices: list[DeviceIdVO] = []

    async def save(self, entity: AuthSession) -> AuthSession:
        self.store[str(entity.id)] = entity
        return entity

    async def batch_save(self, entities: list[AuthSession]) -> list[AuthSession]:
        for entity in entities:
            await self.save(entity)
        return entities

    async def get_by_id(self, _id: IdVO) -> AuthSession | None:
        return self.store.get(str(_id))

    async def revoke_active_for_device(self, device_id: DeviceIdVO) -> None:
        self.revoked_for_devices.append(device_id)

    async def get_by_refresh_token_hash(
        self, refresh_token_hash: str
    ) -> AuthSession | None:
        return next(
            (
                s
                for s in self.store.values()
                if s.refresh_token_hash == refresh_token_hash
            ),
            None,
        )


class FakeEmailLoginChallengeStore(IEmailLoginChallengeStore):
    def __init__(self, *, consume_result: bool = True) -> None:
        self.consume_result = consume_result
        self.consume_calls: list[tuple[UserEmailVO, str]] = []

    async def consume(self, *, email: UserEmailVO, code_hash: str) -> bool:
        self.consume_calls.append((email, code_hash))
        return self.consume_result

    async def save_with_rate_limit(
        self,
        *,
        email: UserEmailVO,
        code_hash: str,
        ttl_seconds: int,
        min_interval_seconds: int,
    ) -> int:
        return ttl_seconds


class FakeVerificationCodeHasher(IVerificationCodeHasher):
    def hash(self, *, email: UserEmailVO, code: str) -> str:
        return f"hashed::{email.value}::{code}"

    def verify(self, *, email: UserEmailVO, code: str, code_hash: str) -> bool:
        return code_hash == self.hash(email=email, code=code)


class FakeAuthSessionService(AuthSessionService):
    def __init__(self) -> None:
        self.issue_calls: list[dict[str, Any]] = []

    async def issue(
        self,
        *,
        principal: Principal,
        role: Any,
        device_id: DeviceIdVO | None = None,
    ) -> IssuedAuthTokens:
        self.issue_calls.append(
            {"principal": principal, "role": role, "device_id": device_id}
        )
        return IssuedAuthTokens(
            access_token="access-token",
            refresh_token="refresh-token",
            access_expires_in=900,
            refresh_expires_in=2_592_000,
        )
