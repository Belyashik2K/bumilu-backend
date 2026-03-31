from pprint import pprint
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7

from app.core.presentation.api.schemas.accept_language import AcceptLanguageDep
from app.core.presentation.api.schemas.location import LocationDep
from app.core.presentation.api.schemas.pagination import OffsetPaginationDep
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api.v1.users.deps import get_user_principal
from app.modules.auth.shared.context import Principal
from app.modules.routes.application.queries.get.handler import GetRouteQueryHandler
from app.modules.routes.application.queries.get.query import GetRouteQuery
from app.modules.routes.application.queries.get_all.handler import (
    GetAllRoutesQueryHandler,
)
from app.modules.routes.application.queries.get_all.query import GetAllRoutesQuery
from app.modules.routes.presentation.api.filters.route_sort import RouteSortFiltersDep
from app.modules.routes.presentation.api.schemas.main import (
    PaginatedRouteCardsResponseSchema,
)

routes_router = APIRouter(
    prefix="/routes",
    tags=["Routes"],
)


@routes_router.get("", responses=generate_responses_for_endpoint())
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


@routes_router.get("/{route_id}", responses=generate_responses_for_endpoint())
@inject
async def get_route_by_id(
    route_id: UUID7,
    handler: FromDishka[GetRouteQueryHandler],
    principal: Annotated[Principal, Depends(get_user_principal)],
    accept_language: AcceptLanguageDep,
) -> None:
    result = await handler(
        GetRouteQuery(
            route_id=route_id,
            language=accept_language.language,
        )
    )
    pprint(result)
    return None
