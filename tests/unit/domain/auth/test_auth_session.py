from collections.abc import Callable
from datetime import (
    datetime,
    timedelta,
)

import pytest
from app.core.domain.value_objects.id import (
    DeviceIdVO,
    PrincipalIdVO,
)
from app.modules.auth.domain.models.auth_session.exceptions import (
    CannotRotateInactiveSession,
    SessionExpirationMustBeInFuture,
)
from app.modules.auth.domain.models.auth_session.model import AuthSession
from app.modules.auth.shared.enums import PrincipalTypeEnum


class TestAuthSessionCreate:
    def test_creates_active_session_with_future_expiration(
        self,
        principal_id: PrincipalIdVO,
        device_id: DeviceIdVO,
        frozen_now: datetime,
    ) -> None:
        expires_at = frozen_now + timedelta(hours=1)

        session = AuthSession.create(
            principal_id=principal_id,
            principal_type=PrincipalTypeEnum.USER,
            refresh_token_hash="hash",
            expires_at=expires_at,
            now=frozen_now,
            device_id=device_id,
        )

        assert session.principal_id == principal_id
        assert session.device_id == device_id
        assert session.expires_at == expires_at
        assert session.revoked_at is None
        assert session.is_active()

    def test_raises_when_expiration_is_in_the_past(
        self,
        principal_id: PrincipalIdVO,
        frozen_now: datetime,
    ) -> None:
        expires_at = frozen_now - timedelta(seconds=1)

        with pytest.raises(SessionExpirationMustBeInFuture):
            AuthSession.create(
                principal_id=principal_id,
                principal_type=PrincipalTypeEnum.USER,
                refresh_token_hash="hash",
                expires_at=expires_at,
                now=frozen_now,
            )

    def test_raises_when_expiration_equals_now(
        self,
        principal_id: PrincipalIdVO,
        frozen_now: datetime,
    ) -> None:
        expires_at = frozen_now

        with pytest.raises(SessionExpirationMustBeInFuture):
            AuthSession.create(
                principal_id=principal_id,
                principal_type=PrincipalTypeEnum.USER,
                refresh_token_hash="hash",
                expires_at=expires_at,
                now=frozen_now,
            )


class TestAuthSessionIsActive:
    def test_is_active_when_not_revoked_and_not_expired(
        self,
        make_auth_session: Callable[..., AuthSession],
    ) -> None:
        session = make_auth_session()

        assert session.is_active() is True

    def test_not_active_when_revoked(
        self,
        make_auth_session: Callable[..., AuthSession],
    ) -> None:
        session = make_auth_session()
        session.revoke()

        assert session.is_active() is False

    def test_not_active_when_expired(
        self,
        make_auth_session: Callable[..., AuthSession],
        frozen_now: datetime,
    ) -> None:
        session = make_auth_session()
        session.expires_at = frozen_now

        assert session.is_active() is False


class TestAuthSessionRevoke:
    def test_sets_revoked_at(
        self,
        make_auth_session: Callable[..., AuthSession],
        frozen_now: datetime,
    ) -> None:
        session = make_auth_session()

        session.revoke()

        assert session.revoked_at == frozen_now

    def test_is_idempotent(
        self,
        make_auth_session: Callable[..., AuthSession],
    ) -> None:
        session = make_auth_session()
        session.revoke()
        first_revoked_at = session.revoked_at

        session.revoke()

        assert session.revoked_at == first_revoked_at


class TestAuthSessionRotate:
    def test_updates_refresh_token_hash_when_active(
        self,
        make_auth_session: Callable[..., AuthSession],
    ) -> None:
        session = make_auth_session(refresh_token_hash="old-hash")

        session.rotate(refresh_token_hash="new-hash")

        assert session.refresh_token_hash == "new-hash"

    def test_raises_when_session_is_revoked(
        self,
        make_auth_session: Callable[..., AuthSession],
    ) -> None:
        session = make_auth_session()
        session.revoke()

        with pytest.raises(CannotRotateInactiveSession):
            session.rotate(refresh_token_hash="new-hash")

    def test_raises_when_session_is_expired(
        self,
        make_auth_session: Callable[..., AuthSession],
        frozen_now: datetime,
    ) -> None:
        session = make_auth_session()
        session.expires_at = frozen_now

        with pytest.raises(CannotRotateInactiveSession):
            session.rotate(refresh_token_hash="new-hash")

    def test_is_noop_when_hash_is_unchanged(
        self,
        make_auth_session: Callable[..., AuthSession],
    ) -> None:
        session = make_auth_session(refresh_token_hash="same-hash")
        original_expires_at = session.expires_at

        session.rotate(
            refresh_token_hash="same-hash",
            new_expires_at=original_expires_at + timedelta(days=1),
        )

        assert session.expires_at == original_expires_at

    def test_updates_expires_at_when_provided(
        self,
        make_auth_session: Callable[..., AuthSession],
    ) -> None:
        session = make_auth_session()
        new_expires_at = session.expires_at + timedelta(days=1)

        session.rotate(refresh_token_hash="new-hash", new_expires_at=new_expires_at)

        assert session.expires_at == new_expires_at

    def test_keeps_expires_at_when_not_provided(
        self,
        make_auth_session: Callable[..., AuthSession],
    ) -> None:
        session = make_auth_session()
        original_expires_at = session.expires_at

        session.rotate(refresh_token_hash="new-hash")

        assert session.expires_at == original_expires_at


class TestAuthSessionPrincipalType:
    def test_is_staff_session_for_staff_principal(
        self,
        make_auth_session: Callable[..., AuthSession],
    ) -> None:
        session = make_auth_session(principal_type=PrincipalTypeEnum.STAFF)

        assert session.is_staff_session() is True
        assert session.is_user_session() is False

    def test_is_user_session_for_user_principal(
        self,
        make_auth_session: Callable[..., AuthSession],
    ) -> None:
        session = make_auth_session(principal_type=PrincipalTypeEnum.USER)

        assert session.is_user_session() is True
        assert session.is_staff_session() is False
