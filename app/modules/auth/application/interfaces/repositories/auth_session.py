from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.shared.domain.value_objects.id import (
    DeviceIdVO,
    SessionIdVO,
)
from app.modules.auth.domain.models.auth_session import AuthSession


class IAuthSessionRepository(IBaseRepository[AuthSession, SessionIdVO], ABC):
    @abstractmethod
    async def revoke_active_for_device(
        self,
        device_id: DeviceIdVO,
    ) -> None: ...
