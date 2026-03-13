from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.core.shared.domain.value_objects.id import PrincipalIdVO
from app.modules.auth.application.interfaces.repositories.principal import (
    IPrincipalRepository,
)
from app.modules.auth.domain.models.principal import Principal
from app.modules.auth.infrastructure.database.models import PrincipalModel


class SQLAlchemyPrincipalRepository(
    IPrincipalRepository,
    SQLAlchemyBaseRepository[Principal, PrincipalModel],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_class=PrincipalModel)

    def _to_data(self, entity: Principal) -> PrincipalModel:
        return PrincipalModel(
            id=entity.id.value,
            type=entity.type,
        )

    def _to_entity(self, data: PrincipalModel) -> Principal:
        return Principal(
            id=PrincipalIdVO.from_uuid(data.id),
            type=data.type,
        )
