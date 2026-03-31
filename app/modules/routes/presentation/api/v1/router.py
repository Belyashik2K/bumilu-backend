from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)

from app.core.presentation.api.schemas.accept_language import AcceptLanguageDep
from app.core.presentation.api.schemas.location import LocationDep
from app.core.presentation.api.schemas.pagination import OffsetPaginationDep
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api.v1.users.deps import get_user_principal
from app.modules.auth.shared.context import Principal
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
