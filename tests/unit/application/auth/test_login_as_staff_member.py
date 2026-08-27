import pytest
from app.modules.auth.application.commands.staff.login.command import (
    LoginAsStaffMemberCommand,
)
from app.modules.auth.application.commands.staff.login.exceptions import (
    InvalidCredentials,
    PrincipalNotFound,
)
from app.modules.auth.application.commands.staff.login.handler import (
    LoginAsStaffMemberCommandHandler,
)
from app.modules.auth.domain.models.principal import Principal
from app.modules.auth.shared.enums import PrincipalTypeEnum
from app.modules.staff.domain.models.staff_member import StaffMember
from app.modules.staff.domain.value_objects.staff_email import StaffMemberEmailVO
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum

from tests.unit.application.auth.fakes import (
    FakeAuthSessionService,
    FakePrincipalRepository,
    FakeStaffMemberRepository,
    FakeStaffPasswordHasher,
)


class TestLoginAsStaffMemberCommandHandler:
    async def test_bootstraps_first_staff_member_as_owner(
        self,
        login_as_staff_member_handler: LoginAsStaffMemberCommandHandler,
        staff_member_repository: FakeStaffMemberRepository,
        principal_repository: FakePrincipalRepository,
        auth_session_service: FakeAuthSessionService,
    ) -> None:
        command = LoginAsStaffMemberCommand(
            email="owner@bumilu.ru", password="Str0ng!Pass"
        )

        result = await login_as_staff_member_handler.handle(command)

        assert result.account.email == "owner@bumilu.ru"
        assert result.account.role == StaffRoleEnum.OWNER
        assert staff_member_repository.store
        created = next(iter(staff_member_repository.store.values()))
        assert created.role == StaffRoleEnum.OWNER
        assert principal_repository.store
        assert auth_session_service.issue_calls[0]["role"] == StaffRoleEnum.OWNER

    async def test_logs_in_existing_staff_member_with_correct_password(
        self,
        login_as_staff_member_handler: LoginAsStaffMemberCommandHandler,
        staff_member_repository: FakeStaffMemberRepository,
        principal_repository: FakePrincipalRepository,
        staff_password_hasher: FakeStaffPasswordHasher,
    ) -> None:
        principal = Principal.create(type=PrincipalTypeEnum.STAFF)
        member = StaffMember.create(
            id=principal.id,
            name="Support",
            email=StaffMemberEmailVO.from_string("support@bumilu.ru"),
            password_hash=staff_password_hasher.hash("Correct!Pass1"),
            role=StaffRoleEnum.SUPPORT,
        )
        await principal_repository.save(principal)
        await staff_member_repository.save(member)

        command = LoginAsStaffMemberCommand(
            email="support@bumilu.ru", password="Correct!Pass1"
        )
        result = await login_as_staff_member_handler.handle(command)

        assert result.account.id == str(principal.id)
        assert result.account.role == StaffRoleEnum.SUPPORT

    async def test_raises_when_existing_staff_member_password_is_wrong(
        self,
        login_as_staff_member_handler: LoginAsStaffMemberCommandHandler,
        staff_member_repository: FakeStaffMemberRepository,
        principal_repository: FakePrincipalRepository,
        staff_password_hasher: FakeStaffPasswordHasher,
    ) -> None:
        principal = Principal.create(type=PrincipalTypeEnum.STAFF)
        member = StaffMember.create(
            id=principal.id,
            name="Support",
            email=StaffMemberEmailVO.from_string("support@bumilu.ru"),
            password_hash=staff_password_hasher.hash("Correct!Pass1"),
            role=StaffRoleEnum.SUPPORT,
        )
        await principal_repository.save(principal)
        await staff_member_repository.save(member)

        command = LoginAsStaffMemberCommand(
            email="support@bumilu.ru", password="Wrong!Pass1"
        )

        with pytest.raises(InvalidCredentials):
            await login_as_staff_member_handler.handle(command)

    async def test_raises_when_email_unknown_and_staff_already_bootstrapped(
        self,
        login_as_staff_member_handler: LoginAsStaffMemberCommandHandler,
        staff_member_repository: FakeStaffMemberRepository,
        principal_repository: FakePrincipalRepository,
        staff_password_hasher: FakeStaffPasswordHasher,
    ) -> None:
        principal = Principal.create(type=PrincipalTypeEnum.STAFF)
        member = StaffMember.create(
            id=principal.id,
            name="Owner",
            email=StaffMemberEmailVO.from_string("owner@bumilu.ru"),
            password_hash=staff_password_hasher.hash("Correct!Pass1"),
            role=StaffRoleEnum.OWNER,
        )
        await principal_repository.save(principal)
        await staff_member_repository.save(member)

        command = LoginAsStaffMemberCommand(
            email="unknown@bumilu.ru", password="Whatever1!"
        )

        with pytest.raises(InvalidCredentials):
            await login_as_staff_member_handler.handle(command)

    async def test_raises_when_principal_missing_for_existing_staff_member(
        self,
        login_as_staff_member_handler: LoginAsStaffMemberCommandHandler,
        staff_member_repository: FakeStaffMemberRepository,
        staff_password_hasher: FakeStaffPasswordHasher,
    ) -> None:
        orphan_member = StaffMember.create(
            id=Principal.create(type=PrincipalTypeEnum.STAFF).id,
            name="Ghost",
            email=StaffMemberEmailVO.from_string("ghost@bumilu.ru"),
            password_hash=staff_password_hasher.hash("Correct!Pass1"),
            role=StaffRoleEnum.SUPPORT,
        )
        await staff_member_repository.save(orphan_member)

        command = LoginAsStaffMemberCommand(
            email="ghost@bumilu.ru", password="Correct!Pass1"
        )

        with pytest.raises(PrincipalNotFound):
            await login_as_staff_member_handler.handle(command)
