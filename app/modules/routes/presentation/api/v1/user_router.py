from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7
from starlette import status

from app.core.presentation.api.schemas.accept_language import AcceptLanguageDep
from app.core.presentation.api.schemas.location import LocationDep
from app.core.presentation.api.schemas.pagination import OffsetPaginationDep
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.users.deps import (
    get_principal,
    get_user_principal,
)
from app.modules.auth.shared.context import Principal
from app.modules.routes.application.queries.build_route_path.handler import (
    BuildRoutePathForRouteQueryHandler,
)
from app.modules.routes.application.queries.build_route_path.query import (
    BuildRoutePathForRouteQuery,
)
from app.modules.routes.application.queries.get.handler import GetRouteQueryHandler
from app.modules.routes.application.queries.get.query import GetRouteQuery
from app.modules.routes.application.queries.get_all.handler import (
    GetAllRoutesQueryHandler,
)
from app.modules.routes.application.queries.get_all.query import GetAllRoutesQuery
from app.modules.routes.presentation.api.filters.route_sort import RouteSortFiltersDep
from app.modules.routes.presentation.api.schemas.card import (
    PaginatedRouteCardsResponseSchema,
)
from app.modules.routes.presentation.api.schemas.main import (
    BuildRoutePathForRouteRequestSchema,
    RouteSchema,
)
from app.modules.routing.presentation.api.schemas.path import RoutePathSchema

user_routes_router = APIRouter(
    prefix="/routes", tags=["Routes"], dependencies=[Depends(security)]
)


@user_routes_router.get("", responses=generate_responses_for_endpoint())
@inject
async def get_routes(
    handler: FromDishka[GetAllRoutesQueryHandler],
    principal: Annotated[Principal, Depends(get_user_principal)],
    accept_language: AcceptLanguageDep,
    location: LocationDep,
    filters: RouteSortFiltersDep,
    pagination: OffsetPaginationDep,
) -> PaginatedRouteCardsResponseSchema:
    result = await handler(
        GetAllRoutesQuery(
            language=accept_language.language,
            latitude=location.latitude,
            longitude=location.longitude,
            sort_by=filters.sort_by,
            limit=pagination.limit,
            offset=pagination.offset,
        )
    )
    return PaginatedRouteCardsResponseSchema.model_validate(
        result, from_attributes=True
    )


@user_routes_router.get("/{route_id}", responses=generate_responses_for_endpoint())
@inject
async def get_route_by_id(
    route_id: UUID7,
    handler: FromDishka[GetRouteQueryHandler],
    principal: Annotated[Principal, Depends(get_user_principal)],
    accept_language: AcceptLanguageDep,
) -> RouteSchema:
    result = await handler(
        GetRouteQuery(
            route_id=route_id,
            language=accept_language.language,
        )
    )
    return RouteSchema.model_validate(result, from_attributes=True)


@user_routes_router.get(
    "/{route_id}/route",
    responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED),
)
@inject
async def build_route_path_for_route(
    route_id: UUID7,
    handler: FromDishka[BuildRoutePathForRouteQueryHandler],
    principal: Annotated[Principal, Depends(get_principal)],
    data: BuildRoutePathForRouteRequestSchema,
    accept_language: AcceptLanguageDep,
) -> RoutePathSchema:
    result = await handler(
        BuildRoutePathForRouteQuery(
            route_id=route_id,
            travel_mode=data.travel_mode,
            language=accept_language.language,
        )
    )
    return RoutePathSchema.model_validate(result, from_attributes=True)
