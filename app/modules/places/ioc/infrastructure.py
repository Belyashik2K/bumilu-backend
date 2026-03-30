from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.infrastructure.database.readers.place_category import (
    SQLAlchemyPlaceCategoryReader,
)


class PlacesInfrastructureProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IPlaceCategoryReader)
    async def place_category_reader(
        self, session: AsyncSession
    ) -> SQLAlchemyPlaceCategoryReader:
        return SQLAlchemyPlaceCategoryReader(session=session)
