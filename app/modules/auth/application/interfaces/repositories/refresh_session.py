from abc import ABC

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.shared.domain.value_objects.id import SessionIdVO
from app.modules.auth.domain.models.refresh_session import RefreshSession


class IRefreshSessionRepository(IBaseRepository[RefreshSession, SessionIdVO], ABC): ...
