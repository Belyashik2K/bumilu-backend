from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.shared.domain.value_objects.id import (
    IdVO,
    ReviewIdVO,
    UserIdVO,
)
from app.modules.reviews.domain.models.review import Review
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class IReviewRepository(IBaseRepository[Review], ABC):
    @abstractmethod
    async def get_by_entity_and_author(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: IdVO,
        author_id: UserIdVO,
    ) -> Review | None: ...

    @abstractmethod
    async def get_all_by_entity_excluding_author(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: IdVO,
        author_id: UserIdVO | None,
    ) -> list[Review]: ...

    @abstractmethod
    async def get_all_by_entity(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: IdVO,
    ) -> list[Review]: ...

    @abstractmethod
    async def delete_by_id(
        self,
        review_id: ReviewIdVO,
    ) -> None: ...
