from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.domain.value_objects.id import (
    DeviceIdVO,
)
from app.modules.auth.domain.models.auth_session import AuthSession


class IAuthSessionRepository(IBaseRepository[AuthSession], ABC):
    @abstractmethod
    async def revoke_active_for_device(
        self,
        device_id: DeviceIdVO,
    ) -> None: ...

    @abstractmethod
    async def get_by_refresh_token_hash(
        self,
        refresh_token_hash: str,
    ) -> AuthSession | None: ...
