from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.core.infrastructure.database.exception_catcher import (
    sqlalchemy_exception_catcher,
)
from app.core.shared.domain.value_objects.id import (
    PrincipalIdVO,
)
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.domain.models.user import User
from app.modules.users.domain.value_objects import UserEmailVO
from app.modules.users.infrastructure.database.models import UserModel


class SQLAlchemyUserRepository(
    IUserRepository, SQLAlchemyBaseRepository[User, UserModel]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserModel)  # TODO: Fix type hints

    def _to_entity(self, data: UserModel) -> User:
        return User(
            id=PrincipalIdVO.from_uuid(data.id),
            email=UserEmailVO.from_string(data.email) if data.email else None,
            email_verified_at=data.email_verified_at,
            role=data.role,
        )

    def _to_data(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id.value,
            email=entity.email.value if entity.email else None,
            email_verified_at=entity.email_verified_at,
            role=entity.role,
        )

    @sqlalchemy_exception_catcher
    async def get_by_email(self, email: UserEmailVO) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email.value)
        result = await self.session.execute(stmt)
        user_data = result.scalar_one_or_none()
        if user_data is None:
            return None
        return self._to_entity(user_data)
