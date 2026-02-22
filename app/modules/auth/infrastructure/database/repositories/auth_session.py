from sqlalchemy import (
    func,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.core.shared.domain.value_objects.id import (
    DeviceIdVO,
    SessionIdVO,
    UserIdVO,
)
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.domain.models.auth_session import AuthSession
from app.modules.auth.infrastructure.database.models import AuthSessionModel


class SQLAlchemyAuthSessionRepository(
    IAuthSessionRepository,
    SQLAlchemyBaseRepository[AuthSession, AuthSessionModel],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AuthSessionModel)

    def _to_entity(self, data: AuthSessionModel) -> AuthSession:
        return AuthSession(
            id=SessionIdVO.from_uuid(data.id),
            user_id=UserIdVO.from_uuid(data.user_id),
            device_id=DeviceIdVO.from_uuid(data.device_id),
            refresh_token_hash=data.refresh_token_hash,
            expires_at=data.expires_at,
            revoked_at=data.revoked_at,
        )

    def _to_data(self, entity: AuthSession) -> AuthSessionModel:
        return AuthSessionModel(
            id=entity.id.value,
            user_id=entity.user_id.value,
            device_id=entity.device_id.value,
            refresh_token_hash=entity.refresh_token_hash,
            expires_at=entity.expires_at,
            revoked_at=entity.revoked_at,
        )

    async def revoke_active_for_device(
        self,
        device_id: DeviceIdVO,
    ) -> None:
        stmt = (
            update(AuthSessionModel)
            .where(
                AuthSessionModel.device_id == device_id.value,
                AuthSessionModel.revoked_at.is_(None),
            )
            .values(revoked_at=func.now())
        )
        await self.session.execute(stmt)
        await self.session.flush()
