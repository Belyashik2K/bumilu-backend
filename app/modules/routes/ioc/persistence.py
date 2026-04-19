from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.interfaces.readers.route_translation import (
    IRouteTranslationReader,
)
from app.modules.routes.application.interfaces.repositories.route import (
    IRouteRepository,
)
from app.modules.routes.infrastructure.database.readers.route import (
    SQLAlchemyRouteReader,
)
from app.modules.routes.infrastructure.database.readers.route_translation import (
    SQLAlchemyRouteTranslationReader,
)
from app.modules.routes.infrastructure.database.repositories.route import (
    SQLAlchemyRouteRepository,
)


class RoutesPersistenceProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IRouteReader)
    async def route_reader(self, session: AsyncSession) -> IRouteReader:
        return SQLAlchemyRouteReader(session=session)

    @provide(scope=Scope.REQUEST, provides=IRouteRepository)
    async def route_repository(self, session: AsyncSession) -> IRouteRepository:
        return SQLAlchemyRouteRepository(session=session)

    @provide(scope=Scope.REQUEST, provides=IRouteTranslationReader)
    async def route_translation_reader(
        self, session: AsyncSession
    ) -> IRouteTranslationReader:
        return SQLAlchemyRouteTranslationReader(session=session)
