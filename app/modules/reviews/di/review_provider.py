from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.reviews.application.interfaces.entity_resolver import IEntityResolver
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.use_cases.create import CreateReviewUseCase
from app.modules.reviews.application.use_cases.delete import DeleteReviewUseCase
from app.modules.reviews.application.use_cases.get_all import (
    GetAllReviewsForEntityUseCase,
)
from app.modules.reviews.application.use_cases.update import UpdateReviewUseCase
from app.modules.reviews.infrastructure.database.repositories.review import (
    SQLAlchemyReviewRepository,
)
from app.modules.reviews.infrastructure.entity_resolver import EntityResolver


class ReviewProvider(Provider):
    @provide(scope=Scope.APP, provides=IEntityResolver)
    async def review_entity_resolver(
        self,
    ) -> EntityResolver:
        return EntityResolver()

    @provide(scope=Scope.REQUEST, provides=IReviewRepository)
    async def review_repository(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyReviewRepository:
        return SQLAlchemyReviewRepository(
            session=session,
        )

    @provide(scope=Scope.REQUEST)
    async def get_all_reviews_for_entity_uc(
        self,
        review_repository: IReviewRepository,
        entity_resolver: IEntityResolver,
    ) -> GetAllReviewsForEntityUseCase:
        return GetAllReviewsForEntityUseCase(
            review_repository=review_repository,
            entity_resolver=entity_resolver,
        )

    @provide(scope=Scope.REQUEST)
    async def create_review_uc(
        self,
        review_repository: IReviewRepository,
        entity_resolver: IEntityResolver,
    ) -> CreateReviewUseCase:
        return CreateReviewUseCase(
            review_repository=review_repository,
            entity_resolver=entity_resolver,
        )

    @provide(scope=Scope.REQUEST)
    async def update_review_uc(
        self,
        review_repository: IReviewRepository,
    ) -> UpdateReviewUseCase:
        return UpdateReviewUseCase(
            review_repository=review_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def delete_review_uc(
        self,
        review_repository: IReviewRepository,
    ) -> DeleteReviewUseCase:
        return DeleteReviewUseCase(
            review_repository=review_repository,
        )
