from uuid import uuid4

import pytest
from app.core.domain.value_objects.id import DeviceIdVO
from app.core.enums import DevicePlatformEnum, UserRoleEnum
from app.modules.auth.application.commands.user.email.verify_code.command import (
    VerifyEmailCodeAtLoginCommand,
)
from app.modules.auth.application.commands.user.email.verify_code.exceptions import (
    InvalidEmailVerificationCode,
)
from app.modules.auth.application.commands.user.email.verify_code.handler import (
    VerifyEmailCodeAtLoginCommandHandler,
)
from app.modules.auth.domain.models.device import Device
from app.modules.auth.domain.models.principal import Principal
from app.modules.auth.shared.enums import PrincipalTypeEnum
from app.modules.users.domain.models.user import User
from app.modules.users.domain.value_objects import UserEmailVO

from tests.unit.application.auth.fakes import (
    FakeAuthSessionRepository,
    FakeAuthSessionService,
    FakeDeviceRepository,
    FakeEmailLoginChallengeStore,
    FakePrincipalRepository,
    FakeUserRepository,
)


def _make_command(**overrides: object) -> VerifyEmailCodeAtLoginCommand:
    defaults: dict[str, object] = {
        "email": "someone@gmail.com",
        "code": "123456",
        "device_id": uuid4(),
        "device_platform": DevicePlatformEnum.ANDROID,
        "device_name": "Pixel 9",
        "app_version": "1.0.0",
    }
    defaults.update(overrides)
    return VerifyEmailCodeAtLoginCommand(**defaults)  # type: ignore[arg-type]


class TestVerifyEmailCodeAtLoginCommandHandler:
    async def test_raises_when_code_is_invalid(
        self,
        verify_email_code_at_login_handler: VerifyEmailCodeAtLoginCommandHandler,
        challenge_store: FakeEmailLoginChallengeStore,
    ) -> None:
        challenge_store.consume_result = False

        with pytest.raises(InvalidEmailVerificationCode):
            await verify_email_code_at_login_handler.handle(_make_command())

    async def test_creates_new_user_and_device_on_first_login(
        self,
        verify_email_code_at_login_handler: VerifyEmailCodeAtLoginCommandHandler,
        user_repository: FakeUserRepository,
        device_repository: FakeDeviceRepository,
        principal_repository: FakePrincipalRepository,
        auth_session_repository: FakeAuthSessionRepository,
    ) -> None:
        device_id = uuid4()
        command = _make_command(email="new-user@gmail.com", device_id=device_id)

        result = await verify_email_code_at_login_handler.handle(command)

        assert result.account.email == "new-user@gmail.com"
        assert result.account.role == UserRoleEnum.USER
        assert len(user_repository.store) == 1
        assert len(principal_repository.store) == 1
        assert DeviceIdVO(device_id) in {d.id for d in device_repository.store.values()}
        assert auth_session_repository.revoked_for_devices == []

    async def test_reuses_existing_user_and_revokes_sessions_for_known_device(
        self,
        verify_email_code_at_login_handler: VerifyEmailCodeAtLoginCommandHandler,
        user_repository: FakeUserRepository,
        device_repository: FakeDeviceRepository,
        principal_repository: FakePrincipalRepository,
        auth_session_repository: FakeAuthSessionRepository,
        auth_session_service: FakeAuthSessionService,
    ) -> None:
        principal = Principal.create(type=PrincipalTypeEnum.USER)
        email = UserEmailVO.from_string("returning@gmail.com")
        user = User.create_user(id=principal.id, email=email)
        await principal_repository.save(principal)
        await user_repository.save(user)

        raw_device_id = uuid4()
        device = Device.create(
            device_id=DeviceIdVO(raw_device_id),
            platform=DevicePlatformEnum.ANDROID,
            app_version="1.0.0",
        )
        await device_repository.save(device)

        command = _make_command(email="returning@gmail.com", device_id=raw_device_id)
        result = await verify_email_code_at_login_handler.handle(command)

        assert result.account.id == str(principal.id)
        assert len(user_repository.store) == 1
        assert auth_session_repository.revoked_for_devices == [
            DeviceIdVO(raw_device_id)
        ]
        assert auth_session_service.issue_calls[0]["principal"] is principal

    async def test_registers_new_device_when_user_exists_but_device_unknown(
        self,
        verify_email_code_at_login_handler: VerifyEmailCodeAtLoginCommandHandler,
        user_repository: FakeUserRepository,
        device_repository: FakeDeviceRepository,
        principal_repository: FakePrincipalRepository,
        auth_session_repository: FakeAuthSessionRepository,
    ) -> None:
        principal = Principal.create(type=PrincipalTypeEnum.USER)
        email = UserEmailVO.from_string("returning@gmail.com")
        user = User.create_user(id=principal.id, email=email)
        await principal_repository.save(principal)
        await user_repository.save(user)

        new_device_id = uuid4()
        command = _make_command(email="returning@gmail.com", device_id=new_device_id)

        await verify_email_code_at_login_handler.handle(command)

        assert len(device_repository.store) == 1
        assert auth_session_repository.revoked_for_devices == []
