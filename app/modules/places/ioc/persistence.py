from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.interfaces.readers.place_translation import (
    IPlaceTranslationReader,
)
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)
from app.modules.places.application.interfaces.repositories.place_category_translation import (
    IPlaceCategoryTranslationRepository,
)
from app.modules.places.application.interfaces.repositories.place_translation import (
    IPlaceTranslationRepository,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.application.queries.categories.shared.readers.place_category_translation import (
    IPlaceCategoryTranslationReader,
)
from app.modules.places.infrastructure.database.readers.place import (
    SQLAlchemyPlaceReader,
)
from app.modules.places.infrastructure.database.readers.place_category import (
    SQLAlchemyPlaceCategoryReader,
)
from app.modules.places.infrastructure.database.readers.place_category_translation import (
    SQLAlchemyPlaceCategoryTranslationReader,
)
from app.modules.places.infrastructure.database.repositories.place import (
    SQLAlchemyPlaceRepository,
)
from app.modules.places.infrastructure.database.repositories.place_category import (
    SQLAlchemyPlaceCategoryRepository,
)
from app.modules.places.infrastructure.database.repositories.place_category_translation import (
    SQLAlchemyPlaceCategoryTranslationRepository,
)
from app.modules.places.infrastructure.database.repositories.place_translation_repository import (
    SQLAlchemyPlaceTranslationRepository,
)


class SQLAlchemyPlaceTranslationReader:
    pass


class PlacesPersistenceProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IPlaceReader)
    async def place_reader(self, session: AsyncSession) -> SQLAlchemyPlaceReader:
        return SQLAlchemyPlaceReader(session=session)

    @provide(scope=Scope.REQUEST, provides=IPlaceRepository)
    async def place_repository(
        self, session: AsyncSession
    ) -> SQLAlchemyPlaceRepository:
        return SQLAlchemyPlaceRepository(session=session)

    @provide(scope=Scope.REQUEST, provides=IPlaceTranslationReader)
    async def place_translation_reader(
        self, session: AsyncSession
    ) -> SQLAlchemyPlaceTranslationReader:
        return SQLAlchemyPlaceTranslationReader()

    @provide(scope=Scope.REQUEST, provides=IPlaceTranslationRepository)
    async def place_translation_repository(
        self, session: AsyncSession
    ) -> SQLAlchemyPlaceTranslationRepository:
        return SQLAlchemyPlaceTranslationRepository(session=session)

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

    @provide(scope=Scope.REQUEST, provides=IPlaceCategoryTranslationReader)
    async def place_category_translation_reader(
        self, session: AsyncSession
    ) -> SQLAlchemyPlaceCategoryTranslationReader:
        return SQLAlchemyPlaceCategoryTranslationReader(session=session)

    @provide(scope=Scope.REQUEST, provides=IPlaceCategoryTranslationRepository)
    async def place_category_translation_repository(
        self, session: AsyncSession
    ) -> SQLAlchemyPlaceCategoryTranslationRepository:
        return SQLAlchemyPlaceCategoryTranslationRepository(session=session)
