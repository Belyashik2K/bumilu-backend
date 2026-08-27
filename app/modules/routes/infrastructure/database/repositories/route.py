from uuid import UUID

from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.domain.value_objects.id import (
    PlaceIdVO,
    RouteIdVO,
    RoutePointIdVO,
    RouteTranslationIdVO,
)
from app.modules.routes.application.interfaces.repositories.route import (
    IRouteRepository,
    RouteLoadOptions,
)
from app.modules.routes.domain.models.route.model import Route
from app.modules.routes.domain.models.route_point.model import RoutePoint
from app.modules.routes.domain.models.route_translation.model import RouteTranslation
from app.modules.routes.domain.value_objects.description.object import (
    RouteDescriptionVO,
)
from app.modules.routes.domain.value_objects.point_index.object import RoutePointIndexVO
from app.modules.routes.domain.value_objects.short_description.object import (
    RouteShortDescriptionVO,
)
from app.modules.routes.domain.value_objects.title.object import RouteTitleVO
from app.modules.routes.infrastructure.database.models import (
    RouteModel,
    RoutePointModel,
    RouteTranslationModel,
)


class RouteDataMapper:
    @staticmethod
    def to_domain(
        model: RouteModel,
        *,
        load_options: RouteLoadOptions | None = None,
    ) -> Route:
        options = load_options or RouteLoadOptions()

        return Route(
            id=RouteIdVO(model.id),
            status=model.status,
            _points=(
                RouteDataMapper._map_points_to_domain(model.points)
                if options.points
                else None
            ),
            _translations=(
                RouteDataMapper._map_translations_to_domain(model.translations)
                if options.translations
                else None
            ),
        )

    @staticmethod
    def _map_points_to_domain(models: list[RoutePointModel]) -> list[RoutePoint]:
        return [
            RoutePoint(
                id=RoutePointIdVO(model.id),
                route_id=RouteIdVO(model.route_id),
                place_id=PlaceIdVO(model.place_id),
                index=RoutePointIndexVO(model.point_index),
            )
            for model in sorted(models, key=lambda x: x.point_index)
        ]

    @staticmethod
    def _map_translations_to_domain(
        models: list[RouteTranslationModel],
    ) -> list[RouteTranslation]:
        return [
            RouteTranslation(
                id=RouteTranslationIdVO(model.id),
                route_id=RouteIdVO(model.route_id),
                language_code=model.language_code,
                title=RouteTitleVO(model.title),
                short_description=RouteShortDescriptionVO(model.short_description),
                description=RouteDescriptionVO(model.description),
            )
            for model in models
        ]

    @staticmethod
    def sync_domain_to_model(entity: Route, model: RouteModel) -> None:
        model.status = entity.status

        if entity._translations is not None:
            RouteDataMapper._merge_translations(entity, model)

    @staticmethod
    def _merge_translations(entity: Route, model: RouteModel) -> None:
        domain_items = entity._translations
        assert domain_items is not None

        domain_ids = {item.id.value for item in domain_items}

        model.translations[:] = [
            orm_item for orm_item in model.translations if orm_item.id in domain_ids
        ]

        orm_by_id: dict[UUID, RouteTranslationModel] = {
            item.id: item for item in model.translations
        }

        for domain_item in domain_items:
            orm_item = orm_by_id.get(domain_item.id.value)

            if orm_item is None:
                model.translations.append(
                    RouteTranslationModel(
                        id=domain_item.id.value,
                        route_id=entity.id.value,
                        language_code=domain_item.language_code,
                        title=domain_item.title.value,
                        short_description=domain_item.short_description.value,
                        description=domain_item.description.value,
                    )
                )
                continue

            assert domain_item.title.value is not None, "RouteTitleVO.value must be set"
            assert domain_item.short_description.value is not None, (
                "RouteShortDescriptionVO.value must be set"
            )
            assert domain_item.description.value is not None, (
                "RouteDescriptionVO.value must be set"
            )

            orm_item.language_code = domain_item.language_code
            orm_item.title = domain_item.title.value
            orm_item.short_description = domain_item.short_description.value
            orm_item.description = domain_item.description.value

    @staticmethod
    def replace_points(entity: Route, model: RouteModel) -> None:
        domain_items = entity._points
        assert domain_items is not None

        model.points = [
            RoutePointModel(
                id=domain_item.id.value,
                route_id=entity.id.value,
                place_id=domain_item.place_id.value,
                point_index=domain_item.index.value,
            )
            for domain_item in domain_items
        ]


class SQLAlchemyRouteRepository(IRouteRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(
        self,
        route_id: RouteIdVO,
        *,
        options: RouteLoadOptions | None = None,
    ) -> Route | None:
        options = options or RouteLoadOptions()

        stmt = select(RouteModel).where(RouteModel.id == route_id.value)

        load_opts = []
        if options.translations:
            load_opts.append(selectinload(RouteModel.translations))
        if options.points:
            load_opts.append(selectinload(RouteModel.points))

        if load_opts:
            stmt = stmt.options(*load_opts)

        model = await self._session.scalar(stmt)
        if model is None:
            return None

        return RouteDataMapper.to_domain(model, load_options=options)

    async def save(self, entity: Route) -> Route:
        stmt = select(RouteModel).where(RouteModel.id == entity.id.value)

        load_opts = []
        if entity._translations is not None:
            load_opts.append(selectinload(RouteModel.translations))
        if entity._points is not None:
            load_opts.append(selectinload(RouteModel.points))

        if load_opts:
            stmt = stmt.options(*load_opts)

        model = await self._session.scalar(stmt)

        if model is None:
            model = RouteModel(
                id=entity.id.value,
                status=entity.status,
            )
            self._session.add(model)

            if entity._translations is not None:
                model.translations = []
            if entity._points is not None:
                model.points = []

        RouteDataMapper.sync_domain_to_model(entity, model)

        if entity._points is not None:
            model.points.clear()
            await self._session.flush()

            RouteDataMapper.replace_points(entity, model)

        await self._session.flush()

        return RouteDataMapper.to_domain(
            model,
            load_options=RouteLoadOptions(
                translations=entity._translations is not None,
                points=entity._points is not None,
            ),
        )

    async def delete_by_id(self, route_id: RouteIdVO) -> None:
        stmt = delete(RouteModel).where(RouteModel.id == route_id.value)
        await self._session.execute(stmt)
