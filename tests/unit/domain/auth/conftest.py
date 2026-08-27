from collections.abc import Callable
from datetime import (
    UTC,
    datetime,
    timedelta,
)

import pytest
from app.core.domain.value_objects.id import (
    DeviceIdVO,
    PrincipalIdVO,
)
from app.modules.auth.domain.models.auth_session.model import AuthSession
from app.modules.auth.shared.enums import PrincipalTypeEnum

FROZEN_NOW: datetime = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def frozen_now(monkeypatch: pytest.MonkeyPatch) -> datetime:
    monkeypatch.setattr(
        "app.modules.auth.domain.models.auth_session.model.get_current_dt",
        lambda: FROZEN_NOW,
    )
    return FROZEN_NOW


@pytest.fixture
def principal_id() -> PrincipalIdVO:
    return PrincipalIdVO.new()


@pytest.fixture
def device_id() -> DeviceIdVO:
    return DeviceIdVO.new()


@pytest.fixture
def make_auth_session(
    principal_id: PrincipalIdVO,
    device_id: DeviceIdVO,
    frozen_now: datetime,
) -> Callable[..., AuthSession]:
    def _make(
        *,
        principal_type: PrincipalTypeEnum = PrincipalTypeEnum.USER,
        refresh_token_hash: str = "initial-hash",
        expires_at: datetime | None = None,
        now: datetime | None = None,
        device: DeviceIdVO | None = device_id,
    ) -> AuthSession:
        return AuthSession.create(
            principal_id=principal_id,
            principal_type=principal_type,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at or frozen_now + timedelta(hours=1),
            now=now or frozen_now,
            device_id=device,
        )

    return _make
