from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)
from app.modules.places.application.interfaces.repositories.place_category_translation import (
    IPlaceCategoryTranslationRepository,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.infrastructure.database.readers.place import (
    SQLAlchemyPlaceReader,
)
from app.modules.places.infrastructure.database.readers.place_category import (
    SQLAlchemyPlaceCategoryReader,
)
from app.modules.places.infrastructure.database.repositories.place_category import (
    SQLAlchemyPlaceCategoryRepository,
)
from app.modules.places.infrastructure.database.repositories.place_category_translation import (
    SQLAlchemyPlaceCategoryTranslationRepository,
)


class PlacesPersistenceProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IPlaceReader)
    async def place_reader(self, session: AsyncSession) -> SQLAlchemyPlaceReader:
        return SQLAlchemyPlaceReader(session=session)

    @provide(scope=Scope.REQUEST, provides=IPlaceCategoryReader)
    async def place_category_reader(
        self, session: AsyncSession
    ) -> SQLAlchemyPlaceCategoryReader:
        return SQLAlchemyPlaceCategoryReader(session=session)

    @provide(scope=Scope.REQUEST, provides=IPlaceCategoryRepository)
    async def place_category_repository(
        self, session: AsyncSession
    ) -> SQLAlchemyPlaceCategoryRepository:
        return SQLAlchemyPlaceCategoryRepository(session=session)

    @provide(scope=Scope.REQUEST, provides=IPlaceCategoryTranslationRepository)
    async def place_category_translation_repository(
        self, session: AsyncSession
    ) -> SQLAlchemyPlaceCategoryTranslationRepository:
        return SQLAlchemyPlaceCategoryTranslationRepository(session=session)
