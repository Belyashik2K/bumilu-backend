from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.routes.application.interfaces.readers import IRouteReader
from app.modules.routes.infrastructure.database.readers.route import (
    SQLAlchemyRouteReader,
)


class RoutesPersistenceProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IRouteReader)
    async def route_reader(self, session: AsyncSession) -> IRouteReader:
        return SQLAlchemyRouteReader(session=session)
