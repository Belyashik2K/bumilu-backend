from typing import Any
from uuid import UUID

from sqlalchemy import (
    and_,
    func,
    literal,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    contains_eager,
    joinedload,
    selectinload,
    with_loader_criteria,
)

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.favourites.infrastructure.database.models import PlaceFavouriteModel
from app.modules.places.application.interfaces.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.dtos import BBox
from app.modules.places.application.queries.places.shared.mappers import (
    PlaceMapPOIMapper,
    PlacePhoneMapper,
    PlacePhotoMapper,
    PlaceReadModelMapper,
    PlaceWorkingDayMapper,
)
from app.modules.places.application.queries.places.shared.models.place_card import (
    AdminPlaceCardReadModel,
    PlaceCardReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_details import (
    AdminPlaceDetailsReadModel,
    PlaceDetailsReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_map_poi import (
    AdminPlaceMapPOIReadModel,
    PlaceMapPOIReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    AdminPlacePhoneReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_photo import (
    AdminPlacePhotoReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_day import (
    PlaceWorkingDayReadModel,
)
from app.modules.places.infrastructure.database.models import (
    PlaceCategoryModel,
    PlaceCategoryTranslationModel,
    PlaceModel,
    PlacePhoneModel,
    PlacePhotoModel,
    PlaceTranslationModel,
    PlaceWorkingDayModel,
)
from app.modules.places.shared.enums.place_photo_status import PlacePhotoStatusEnum
from app.modules.places.shared.enums.place_status import PlaceStatusEnum

from ..query_builders.place import (
    PlaceListFilters,
    SQLAlchemyPlaceQueryBuilder,
)


class SQLAlchemyPlaceReader(IPlaceReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _build_reviews_subquery(place_ids: list[UUID] | None = None):
        return SQLAlchemyPlaceQueryBuilder.build_reviews_subquery(place_ids)

    @staticmethod
    def _build_public_filters(
        *,
        filters: PlaceListFilters,
        language: LanguageEnum,
    ) -> list[Any]:
        return SQLAlchemyPlaceQueryBuilder.build_public_filters(
            filters=filters,
            language=language,
        )

    @staticmethod
    def _build_admin_filters(
        *,
        filters: PlaceListFilters,
        language: LanguageEnum | None = None,
    ) -> list[Any]:
        return SQLAlchemyPlaceQueryBuilder.build_admin_filters(
            filters=filters,
            language=language,
        )

    @staticmethod
    def _build_public_base_stmt(
        *,
        language: LanguageEnum,
        filters: PlaceListFilters,
    ):
        return SQLAlchemyPlaceQueryBuilder.build_public_base_stmt(
            language=language,
            filters=filters,
        )

    @staticmethod
    def _build_public_cards_stmt(
        *,
        language: LanguageEnum,
        filters: PlaceListFilters,
    ):
        return SQLAlchemyPlaceQueryBuilder.build_public_cards_stmt(
            language=language,
            filters=filters,
        )

    @staticmethod
    def _build_admin_cards_stmt(
        *,
        language: LanguageEnum,
        filters: PlaceListFilters,
    ):
        return SQLAlchemyPlaceQueryBuilder.build_admin_cards_stmt(
            language=language,
            filters=filters,
        )

    @staticmethod
    def _build_public_count_stmt(
        *,
        language: LanguageEnum,
        filters: PlaceListFilters,
    ):
        return SQLAlchemyPlaceQueryBuilder.build_public_count_stmt(
            language=language,
            filters=filters,
        )

    @staticmethod
    def _build_admin_count_stmt(
        *,
        language: LanguageEnum,
        filters: PlaceListFilters,
    ):
        return SQLAlchemyPlaceQueryBuilder.build_admin_count_stmt(
            language=language,
            filters=filters,
        )

    async def _paginate_with_total(
        self,
        *,
        items_stmt,
        count_stmt,
        limit: int,
        offset: int,
    ) -> tuple[list[Any], int]:
        total_subquery = count_stmt.scalar_subquery()

        stmt = (
            items_stmt.add_columns(total_subquery.label("total_count"))
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(stmt)
        rows = result.unique().all()

        if not rows:
            total = await self._session.scalar(count_stmt)
            return [], total or 0

        total = rows[0].total_count or 0
        return rows, total

    async def exists(self, place_id: UUID) -> bool:
        stmt = (
            select(func.count())
            .select_from(PlaceModel)
            .where(PlaceModel.id == place_id)
        )
        result = await self._session.execute(stmt)
        count = result.scalar_one()
        return count > 0

    async def count_by_category_id(self, category_id: UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(PlaceModel)
            .where(PlaceModel.category_id == category_id)
        )
        result = await self._session.execute(stmt)
        count = result.scalar_one()
        return count

    async def count_existing_places_by_status(
        self, place_ids: list[UUID], status: PlaceStatusEnum
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(PlaceModel)
            .where(PlaceModel.id.in_(place_ids))
        )

        if status is not None:
            stmt = stmt.where(PlaceModel.status == status)

        result = await self._session.execute(stmt)
        count = result.scalar_one()
        return count

    async def get_by_id(
        self,
        *,
        actor_id: UUID | None = None,
        place_id: UUID,
        translation_language: LanguageEnum,
    ) -> PlaceDetailsReadModel | None:
        if actor_id is None:
            is_favorite_expr = literal(False)
        else:
            is_favorite_expr = (
                select(PlaceFavouriteModel.user_id)
                .where(
                    PlaceFavouriteModel.place_id == PlaceModel.id,
                    PlaceFavouriteModel.user_id == actor_id,
                )
                .exists()
            )

        stmt = (
            select(
                PlaceModel,
                is_favorite_expr.label("is_favorite"),
            )
            .join(PlaceModel.translations)
            .join(PlaceModel.category)
            .join(PlaceCategoryModel.translations)
            .where(
                PlaceTranslationModel.language_code == translation_language,
                PlaceCategoryTranslationModel.language_code == translation_language,
                PlaceModel.status == PlaceStatusEnum.PUBLISHED,
                PlaceModel.id == place_id,
            )
            .options(
                selectinload(PlaceModel.phones),
                selectinload(PlaceModel.working_days).selectinload(
                    PlaceWorkingDayModel.working_hours
                ),
                selectinload(PlaceModel.photos),
                contains_eager(PlaceModel.translations),
                contains_eager(PlaceModel.category).contains_eager(
                    PlaceCategoryModel.translations
                ),
                with_loader_criteria(
                    PlaceModel.photos,
                    PlacePhotoModel.status == PlacePhotoStatusEnum.UPLOADED,
                    include_aliases=True
                )
            )
        )

        result = await self._session.execute(stmt)
        row = result.unique().one_or_none()

        if row is None:
            return None

        place, is_favorite = row
        return PlaceReadModelMapper.map_details(place=place, is_favorite=is_favorite)

    async def get_admin_details_by_id(
        self,
        place_id: UUID,
        optional_translation_language: LanguageEnum,
    ) -> AdminPlaceDetailsReadModel | None:
        stmt = (
            select(PlaceModel, PlaceTranslationModel)
            .outerjoin(
                PlaceTranslationModel,
                and_(
                    PlaceTranslationModel.place_id == PlaceModel.id,
                    PlaceTranslationModel.language_code
                    == optional_translation_language,
                ),
            )
            .options(joinedload(PlaceModel.category))
            .where(PlaceModel.id == place_id)
        )

        result = await self._session.execute(stmt)
        row = result.unique().one_or_none()

        if not row:
            return None

        return PlaceReadModelMapper.map_admin_details(
            place=row.PlaceModel, translation=row.PlaceTranslationModel
        )

    async def get_cards_by_ids(
        self,
        place_ids: list[UUID],
        translation_language: LanguageEnum,
    ) -> list[PlaceCardReadModel]:
        if not place_ids:
            return []

        filters = PlaceListFilters(place_ids=place_ids)

        stmt = self._build_public_cards_stmt(
            language=translation_language,
            filters=filters,
        )

        result = await self._session.execute(stmt)
        rows = result.unique().all()

        cards_by_id: dict[UUID, PlaceCardReadModel] = {
            place.id: PlaceReadModelMapper.map_card(
                place=place,
                rating_average=rating_average,
                reviews_count=reviews_count,
            )
            for place, rating_average, reviews_count in rows
        }

        return [
            cards_by_id[place_id] for place_id in place_ids if place_id in cards_by_id
        ]

    async def get_all(
        self,
        *,
        title_like: str | None,
        category_slug: str | None,
        translation_language: LanguageEnum,
        limit: int,
        offset: int,
    ) -> PageReadModel[PlaceCardReadModel]:
        filters = PlaceListFilters(
            title_like=title_like,
            category_slug=category_slug,
        )

        items_stmt = self._build_public_cards_stmt(
            language=translation_language,
            filters=filters,
        ).order_by(PlaceModel.id)

        count_stmt = self._build_public_count_stmt(
            language=translation_language,
            filters=filters,
        )

        rows, total = await self._paginate_with_total(
            items_stmt=items_stmt,
            count_stmt=count_stmt,
            limit=limit,
            offset=offset,
        )

        return PageReadModel(
            items=[
                PlaceReadModelMapper.map_card(
                    place=place,
                    rating_average=rating_average,
                    reviews_count=reviews_count,
                )
                for place, rating_average, reviews_count, _ in rows
            ],
            total=total,
        )

    async def admin_get_all(
        self,
        *,
        title_like: str | None,
        category_slug: str | None,
        optional_translation_language: LanguageEnum,
        limit: int,
        offset: int,
    ) -> PageReadModel[AdminPlaceCardReadModel]:
        filters = PlaceListFilters(
            title_like=title_like,
            category_slug=category_slug,
        )

        items_stmt = self._build_admin_cards_stmt(
            language=optional_translation_language,
            filters=filters,
        ).order_by(PlaceModel.id)

        count_stmt = self._build_admin_count_stmt(
            language=optional_translation_language,
            filters=filters,
        )

        rows, total = await self._paginate_with_total(
            items_stmt=items_stmt,
            count_stmt=count_stmt,
            limit=limit,
            offset=offset,
        )

        return PageReadModel(
            items=[
                PlaceReadModelMapper.map_admin_card(
                    place=place,
                    translation=translation,
                    rating_average=rating_average,
                    reviews_count=reviews_count,
                )
                for place, translation, rating_average, reviews_count, _ in rows
            ],
            total=total,
        )

    async def list_poi_in_bounds(
        self,
        *,
        bounds: BBox,
        translation_language: LanguageEnum,
        limit: int,
    ) -> list[PlaceMapPOIReadModel]:
        bbox = func.ST_MakeEnvelope(
            bounds.west,
            bounds.south,
            bounds.east,
            bounds.north,
            4326,
        )

        stmt = (
            select(PlaceModel)
            .join(PlaceModel.translations)
            .join(PlaceModel.category)
            .join(PlaceCategoryModel.translations)
            .where(
                PlaceTranslationModel.language_code == translation_language,
                PlaceCategoryTranslationModel.language_code == translation_language,
                PlaceModel.status == PlaceStatusEnum.PUBLISHED,
                PlaceModel.location.op("&&")(bbox),
                func.ST_Intersects(PlaceModel.location, bbox),
            )
            .options(
                contains_eager(PlaceModel.translations),
                contains_eager(PlaceModel.category).contains_eager(
                    PlaceCategoryModel.translations
                ),
            )
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        rows = result.unique().all()

        return [PlaceMapPOIMapper.map(place=row.PlaceModel) for row in rows]

    async def list_admin_poi_in_bounds(
        self,
        *,
        bounds: BBox,
        optional_translation_language: LanguageEnum,
        limit: int,
    ) -> list[AdminPlaceMapPOIReadModel]:
        bbox = func.ST_MakeEnvelope(
            bounds.west,
            bounds.south,
            bounds.east,
            bounds.north,
            4326,
        )

        stmt = (
            select(PlaceModel, PlaceTranslationModel)
            .outerjoin(
                PlaceTranslationModel,
                and_(
                    PlaceTranslationModel.place_id == PlaceModel.id,
                    PlaceTranslationModel.language_code
                    == optional_translation_language,
                ),
            )
            .options(joinedload(PlaceModel.category))
            .where(
                PlaceModel.location.op("&&")(bbox),
                func.ST_Intersects(PlaceModel.location, bbox),
            )
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        rows = result.unique().all()

        return [
            PlaceMapPOIMapper.map_admin(
                place=place,
                translation=translation,
            )
            for place, translation in rows
        ]

    async def get_admin_photos_by_id(
        self,
        place_id: UUID,
    ) -> list[AdminPlacePhotoReadModel]:
        stmt = select(PlacePhotoModel).where(
            PlacePhotoModel.place_id == place_id,
            PlacePhotoModel.status.in_(
                [PlacePhotoStatusEnum.READY, PlacePhotoStatusEnum.UPLOADED]
            ),
        )

        result = await self._session.execute(stmt)
        photos = result.scalars().all()

        return [PlacePhotoMapper.map_admin(photo=photo) for photo in photos]

    async def get_admin_phones_by_id(
        self,
        place_id: UUID,
    ) -> list[AdminPlacePhoneReadModel]:
        stmt = select(PlacePhoneModel).where(PlacePhoneModel.place_id == place_id)

        result = await self._session.execute(stmt)
        phones = result.scalars().all()

        return [PlacePhoneMapper.map_admin(phone=phone) for phone in phones]

    async def get_working_days_by_id(
        self,
        place_id: UUID,
    ) -> list[PlaceWorkingDayReadModel]:
        stmt = (
            select(PlaceWorkingDayModel)
            .where(PlaceWorkingDayModel.place_id == place_id)
            .order_by(PlaceWorkingDayModel.weekday)
            .options(selectinload(PlaceWorkingDayModel.working_hours))
        )

        result = await self._session.execute(stmt)
        working_days = result.scalars().all()

        return [
            PlaceWorkingDayMapper.map(working_day=working_day)
            for working_day in working_days
        ]

    async def get_working_day_by_weekday(
        self,
        place_id: UUID,
        weekday: int,
    ) -> PlaceWorkingDayReadModel | None:
        stmt = (
            select(PlaceWorkingDayModel)
            .where(
                PlaceWorkingDayModel.place_id == place_id,
                PlaceWorkingDayModel.weekday == weekday,
            )
            .options(selectinload(PlaceWorkingDayModel.working_hours))
        )

        result = await self._session.execute(stmt)
        working_day = result.scalar_one_or_none()

        if not working_day:
            return None

        return PlaceWorkingDayMapper.map(working_day=working_day)
