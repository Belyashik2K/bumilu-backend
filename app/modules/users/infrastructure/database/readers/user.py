from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.application.queries.shared.readers import IUserReader
from app.modules.users.application.queries.shared.views import UserInfoView
from app.modules.users.infrastructure.database.models import UserModel


class SQLAlchemyUserReader(IUserReader):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> Optional["UserInfoView"]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None
        return UserInfoView(
            id=user.id,
            email=user.email,
            role=user.role,
        )
