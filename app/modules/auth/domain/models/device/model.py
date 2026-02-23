from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Self

from app.core.shared.domain.value_objects.id import (
    DeviceIdVO,
    UserIdVO,
)
from app.core.shared.enums import DevicePlatformEnum
from app.core.shared.utils import get_current_dt
from app.modules.auth.domain.models.device.exceptions import (
    DeviceAlreadyAttachedToDifferentGuestUser,
)


@dataclass(slots=True, kw_only=True)
class Device:
    id: DeviceIdVO
    platform: DevicePlatformEnum
    name: str | None = field(default=None)
    app_version: str
    guest_user_id: UserIdVO | None = field(default=None)
    last_seen_at: datetime = field(default_factory=get_current_dt)

    def touch(self) -> None:
        self.last_seen_at = get_current_dt()

    def update_name(self, name: str | None) -> None:
        if name is None or self.name == name:
            return
        self.name = name

    def update_app_version(self, app_version: str) -> None:
        if not app_version or self.app_version == app_version:
            return
        self.app_version = app_version

    def sync_client_state(
        self,
        *,
        app_version: str,
        name: str | None = None,
    ) -> None:
        self.update_name(name)
        self.update_app_version(app_version)
        self.touch()

    def attach_guest_user(self, guest_user_id: UserIdVO) -> None:
        if self.guest_user_id is not None and self.guest_user_id != guest_user_id:
            raise DeviceAlreadyAttachedToDifferentGuestUser()
        if self.guest_user_id == guest_user_id:
            return
        self.guest_user_id = guest_user_id

    def has_guest_user(self) -> bool:
        return self.guest_user_id is not None

    @classmethod
    def create(
        cls,
        *,
        device_id: DeviceIdVO,
        platform: DevicePlatformEnum,
        app_version: str,
        guest_user_id: UserIdVO | None = None,
        name: str | None = None,
    ) -> Self:
        return cls(
            id=device_id,
            platform=platform,
            name=name,
            app_version=app_version,
            guest_user_id=guest_user_id,
        )
