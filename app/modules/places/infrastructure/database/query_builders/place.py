from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import (
    Float,
    and_,
    func,
    select,
)
from sqlalchemy.orm import (
    contains_eager,
    joinedload,
    selectinload,
    with_loader_criteria,
)

from app.core.enums import LanguageEnum
from app.modules.places.infrastructure.database.models import (
    PlaceCategoryModel,
    PlaceCategoryTranslationModel,
    PlaceModel,
    PlacePhotoModel,
    PlaceTranslationModel,
    PlaceWorkingDayModel,
)
from app.modules.places.shared.enums.place_photo_status import PlacePhotoStatusEnum
from app.modules.places.shared.enums.place_status import PlaceStatusEnum
from app.modules.reviews.infrastructure.database.models import ReviewModel
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


@dataclass(slots=True)
class PlaceListFilters:
    title_like: str | None = None
    category_slug: str | None = None
    place_ids: list[UUID] | None = None
    status: PlaceStatusEnum | None = None


class SQLAlchemyPlaceQueryBuilder:
    @staticmethod
    def build_reviews_subquery(place_ids: list[UUID] | None = None):
        stmt = select(
            ReviewModel.entity_id.label("place_id"),
            func.avg(ReviewModel.rating).cast(Float).label("rating_average"),
            func.count(ReviewModel.id).label("reviews_count"),
        ).where(ReviewModel.entity_type == ReviewEntityTypeEnum.PLACE)

        if place_ids:
            stmt = stmt.where(ReviewModel.entity_id.in_(place_ids))

        return stmt.group_by(ReviewModel.entity_id).subquery()

    @staticmethod
    def build_public_filters(
        *,
        filters: PlaceListFilters,
        language: LanguageEnum,
    ) -> list[Any]:
        conditions: list[Any] = [
            PlaceTranslationModel.language_code == language,
            PlaceCategoryTranslationModel.language_code == language,
            PlaceModel.status == PlaceStatusEnum.PUBLISHED,
        ]

        if filters.title_like:
            conditions.append(
                PlaceModel.translations.any(
                    PlaceTranslationModel.title.ilike(f"%{filters.title_like}%"),
                )
            )

        if filters.category_slug:
            conditions.append(PlaceCategoryModel.slug == filters.category_slug)

        if filters.place_ids:
            conditions.append(PlaceModel.id.in_(filters.place_ids))

        return conditions

    @staticmethod
    def build_admin_filters(
        *,
        filters: PlaceListFilters,
        language: LanguageEnum | None = None,
    ) -> list[Any]:
        conditions: list[Any] = []

        if filters.title_like:
            if language is None:
                conditions.append(
                    PlaceModel.translations.any(
                        PlaceTranslationModel.title.ilike(f"%{filters.title_like}%")
                    )
                )
            else:
                conditions.append(
                    PlaceModel.translations.any(
                        and_(
                            PlaceTranslationModel.language_code == language,
                            PlaceTranslationModel.title.ilike(
                                f"%{filters.title_like}%"
                            ),
                        )
                    )
                )

        if filters.category_slug:
            conditions.append(PlaceCategoryModel.slug == filters.category_slug)

        if filters.place_ids:
            conditions.append(PlaceModel.id.in_(filters.place_ids))

        if filters.status is not None:
            conditions.append(PlaceModel.status == filters.status)

        return conditions

    @classmethod
    def build_public_base_stmt(
        cls,
        *,
        language: LanguageEnum,
        filters: PlaceListFilters,
    ):
        return (
            select(PlaceModel)
            .join(PlaceModel.translations)
            .join(PlaceModel.category)
            .join(PlaceCategoryModel.translations)
            .where(*cls.build_public_filters(filters=filters, language=language))
            .options(
                selectinload(PlaceModel.working_days).selectinload(
                    PlaceWorkingDayModel.working_hours
                ),
                selectinload(PlaceModel.photos),
                with_loader_criteria(
                    PlacePhotoModel,
                    PlacePhotoModel.status == PlacePhotoStatusEnum.UPLOADED,
                    include_aliases=True,
                ),
                contains_eager(PlaceModel.translations),
                contains_eager(PlaceModel.category).contains_eager(
                    PlaceCategoryModel.translations
                ),
            )
        )

    @classmethod
    def build_public_cards_stmt(
        cls,
        *,
        language: LanguageEnum,
        filters: PlaceListFilters,
    ):
        reviews_subq = cls.build_reviews_subquery(filters.place_ids)

        return (
            cls.build_public_base_stmt(language=language, filters=filters)
            .outerjoin(reviews_subq, reviews_subq.c.place_id == PlaceModel.id)
            .add_columns(
                reviews_subq.c.rating_average,
                func.coalesce(reviews_subq.c.reviews_count, 0).label("reviews_count"),
            )
        )

    @classmethod
    def build_admin_cards_stmt(
        cls,
        *,
        language: LanguageEnum,
        filters: PlaceListFilters,
    ):
        reviews_subq = cls.build_reviews_subquery(filters.place_ids)

        return (
            select(
                PlaceModel,
                PlaceTranslationModel,
                reviews_subq.c.rating_average,
                func.coalesce(reviews_subq.c.reviews_count, 0).label("reviews_count"),
            )
            .join(PlaceModel.category)
            .outerjoin(
                PlaceTranslationModel,
                and_(
                    PlaceTranslationModel.place_id == PlaceModel.id,
                    PlaceTranslationModel.language_code == language,
                ),
            )
            .outerjoin(reviews_subq, reviews_subq.c.place_id == PlaceModel.id)
            .where(*cls.build_admin_filters(filters=filters, language=language))
            .options(joinedload(PlaceModel.category))
        )

    @classmethod
    def build_public_count_stmt(
        cls,
        *,
        language: LanguageEnum,
        filters: PlaceListFilters,
    ):
        return (
            select(func.count(func.distinct(PlaceModel.id)))
            .select_from(PlaceModel)
            .join(PlaceModel.translations)
            .join(PlaceModel.category)
            .join(PlaceCategoryModel.translations)
            .where(*cls.build_public_filters(filters=filters, language=language))
        )

    @classmethod
    def build_admin_count_stmt(
        cls,
        *,
        language: LanguageEnum,
        filters: PlaceListFilters,
    ):
        stmt = select(func.count(func.distinct(PlaceModel.id))).select_from(PlaceModel)
        stmt = stmt.join(PlaceModel.category)

        return stmt.where(*cls.build_admin_filters(filters=filters, language=language))
