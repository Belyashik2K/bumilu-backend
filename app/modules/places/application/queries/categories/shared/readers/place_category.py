from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.places.application.queries.categories.shared.models.place_category import (
    AdminPlaceCategoryReadModel,
    LocalizedPlaceCategoryReadModel,
)
from app.modules.places.shared.enums.place_category_status import (
    PlaceCategoryStatusEnum,
)


class IPlaceCategoryReader(ABC):
    @abstractmethod
    async def exists(self, slug: str) -> bool: ...

    @abstractmethod
    async def get_admin_by_id(
        self,
        category_id: UUID,
        optional_translation_language: LanguageEnum | None = None,
    ) -> AdminPlaceCategoryReadModel | None: ...

    @abstractmethod
    async def list_public_localized(
        self,
        limit: int,
        offset: int,
        translation_language: LanguageEnum,
        status: PlaceCategoryStatusEnum | None = None,
    ) -> PageReadModel[LocalizedPlaceCategoryReadModel]: ...

    @abstractmethod
    async def list_admin(
        self,
        limit: int,
        offset: int,
        optional_translation_language: LanguageEnum | None = None,
        status: PlaceCategoryStatusEnum | None = None,
    ) -> PageReadModel[AdminPlaceCategoryReadModel]: ...
