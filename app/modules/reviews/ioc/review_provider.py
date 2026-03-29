from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.reviews.application.commands.create import CreateReviewCommandHandler
from app.modules.reviews.application.commands.delete import DeleteReviewCommandHandler
from app.modules.reviews.application.commands.update import UpdateReviewCommandHandler
from app.modules.reviews.application.interfaces.entity_resolver import (
    IReviewEntityResolver,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.queries.get.handler import GetReviewQueryHandler
from app.modules.reviews.application.queries.get_all_by_user.handler import (
    GetAllReviewsByUserQueryHandler,
)
from app.modules.reviews.application.queries.get_all_for_entity.handler import (
    GetAllReviewsForEntityQueryHandler,
)
from app.modules.reviews.application.queries.shared.readers.review import IReviewReader
from app.modules.reviews.infrastructure.database.readers.review import (
    SQLAlchemyReviewReader,
)
from app.modules.reviews.infrastructure.database.repositories.review import (
    SQLAlchemyReviewRepository,
)
from app.modules.reviews.infrastructure.entity_resolver import (
    ReviewEntityResolver,
)
from app.modules.users.application.queries.shared.readers import IUserReader


class ReviewProvider(Provider):
    @provide(scope=Scope.APP, provides=IReviewEntityResolver)
    async def review_entity_resolver(
        self,
    ) -> ReviewEntityResolver:
        return ReviewEntityResolver()

    @provide(scope=Scope.REQUEST, provides=IReviewRepository)
    async def review_repository(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyReviewRepository:
        return SQLAlchemyReviewRepository(
            session=session,
        )

    @provide(scope=Scope.REQUEST, provides=IReviewReader)
    async def review_reader(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyReviewReader:
        return SQLAlchemyReviewReader(
            session=session,
        )

    @provide(scope=Scope.REQUEST)
    async def get_all_reviews_for_entity_handler(
        self,
        review_reader: IReviewReader,
        entity_resolver: IReviewEntityResolver,
    ) -> GetAllReviewsForEntityQueryHandler:
        return GetAllReviewsForEntityQueryHandler(
            review_reader=review_reader,
            entity_resolver=entity_resolver,
        )

    @provide(scope=Scope.REQUEST)
    async def create_review_handler(
        self,
        review_repository: IReviewRepository,
        entity_resolver: IReviewEntityResolver,
        transaction_manager: ITransactionManager,
    ) -> CreateReviewCommandHandler:
        return CreateReviewCommandHandler(
            transaction_manager=transaction_manager,
            review_repository=review_repository,
            entity_resolver=entity_resolver,
        )

    @provide(scope=Scope.REQUEST)
    async def update_review_handler(
        self,
        review_repository: IReviewRepository,
        transaction_manager: ITransactionManager,
    ) -> UpdateReviewCommandHandler:
        return UpdateReviewCommandHandler(
            transaction_manager=transaction_manager,
            review_repository=review_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def delete_review_handler(
        self,
        review_repository: IReviewRepository,
        transaction_manager: ITransactionManager,
    ) -> DeleteReviewCommandHandler:
        return DeleteReviewCommandHandler(
            transaction_manager=transaction_manager,
            review_repository=review_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def get_review_handler(
        self, review_reader: IReviewReader
    ) -> GetReviewQueryHandler:
        return GetReviewQueryHandler(
            review_reader=review_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_all_reviews_by_user_handler(
        self, review_reader: IReviewReader, user_reader: IUserReader
    ) -> GetAllReviewsByUserQueryHandler:
        return GetAllReviewsByUserQueryHandler(
            review_reader=review_reader,
            user_reader=user_reader,
        )
