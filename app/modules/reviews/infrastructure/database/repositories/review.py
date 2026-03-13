from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.core.infrastructure.database.exception_catcher import (
    sqlalchemy_exception_catcher,
)
from app.core.shared.domain.value_objects.id import (
    IdVO,
    PrincipalIdVO,
    ReviewIdVO,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.domain.models.review import Review
from app.modules.reviews.domain.value_objects import (
    ReviewRatingVO,
    ReviewTextVO,
)
from app.modules.reviews.infrastructure.database.models import ReviewModel
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class SQLAlchemyReviewRepository(
    IReviewRepository, SQLAlchemyBaseRepository[Review, ReviewModel]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ReviewModel)

    def _to_entity(self, data: ReviewModel) -> Review:
        return Review(
            id=ReviewIdVO.from_uuid(data.id),
            author_id=PrincipalIdVO.from_uuid(data.author_id),
            entity_type=data.entity_type,
            entity_id=IdVO.from_uuid(data.entity_id),
            text=ReviewTextVO(data.text),
            rating=ReviewRatingVO(data.rating),
        )

    def _to_data(self, entity: Review) -> ReviewModel:
        return ReviewModel(
            id=entity.id.value,
            author_id=entity.author_id.value,
            entity_type=entity.entity_type,
            entity_id=entity.entity_id.value,
            text=entity.text.value,
            rating=entity.rating.value,
        )

    @sqlalchemy_exception_catcher
    async def get_by_entity_and_author(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: IdVO,
        author_id: PrincipalIdVO,
    ) -> Review | None:
        stmt = select(ReviewModel).where(
            ReviewModel.entity_type == entity_type,
            ReviewModel.entity_id == entity_id.value,
            ReviewModel.author_id == author_id.value,
        )
        result = await self.session.execute(stmt)
        review_model = result.scalar_one_or_none()
        if review_model is None:
            return None
        return self._to_entity(review_model)

    @sqlalchemy_exception_catcher
    async def get_all_by_entity_excluding_author(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: IdVO,
        author_id: PrincipalIdVO | None,
    ) -> list[Review]:
        stmt = select(ReviewModel).where(
            ReviewModel.entity_type == entity_type,
            ReviewModel.entity_id == entity_id.value,
        )
        if author_id is not None:
            stmt = stmt.where(ReviewModel.author_id != author_id.value)
        result = await self.session.execute(stmt)
        review_models = result.scalars().all()
        return [self._to_entity(review_model) for review_model in review_models]

    @sqlalchemy_exception_catcher
    async def get_all_by_author(
        self,
        author_id: PrincipalIdVO,
    ) -> list[Review]:
        stmt = select(ReviewModel).where(
            ReviewModel.author_id == author_id.value,
        )
        result = await self.session.execute(stmt)
        review_models = result.scalars().all()
        return [self._to_entity(review_model) for review_model in review_models]

    @sqlalchemy_exception_catcher
    async def get_all_by_entity(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: IdVO,
    ) -> list[Review]:
        stmt = select(ReviewModel).where(
            ReviewModel.entity_type == entity_type,
            ReviewModel.entity_id == entity_id.value,
        )
        result = await self.session.execute(stmt)
        review_models = result.scalars().all()
        return [self._to_entity(review_model) for review_model in review_models]

    @sqlalchemy_exception_catcher
    async def delete_by_id(self, review_id: ReviewIdVO) -> None:
        stmt = delete(ReviewModel).where(
            ReviewModel.id == review_id.value,
        )
        await self.session.execute(stmt)
