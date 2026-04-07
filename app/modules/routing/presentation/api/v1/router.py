from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from app.core.presentation.api.schemas.accept_language import (
    AcceptLanguageDep,
)
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.users.deps import get_user_principal
from app.modules.auth.shared.context import Principal
from app.modules.routing.application.queries.get_route.handler import (
    GetRouteBetweenPointsQueryHandler,
)
from app.modules.routing.application.queries.get_route.query import (
    GetRouteBetweenPointsQuery,
    Waypoint,
)
from app.modules.routing.presentation.api.schemas.main import (
    GetRouteBetweenPointsRequestSchema,
)
from app.modules.routing.presentation.api.schemas.path import RoutePathSchema

routing_router = APIRouter(
    prefix="/routing",
    tags=["Routing"],
    dependencies=[Depends(security)],
)


@routing_router.get(
    "/route", responses=generate_responses_for_endpoint(status.HTTP_501_NOT_IMPLEMENTED)
)
@inject
async def get_route_between_points(
    handler: FromDishka[GetRouteBetweenPointsQueryHandler],
    principal: Annotated[Principal, Depends(get_user_principal)],
    data: GetRouteBetweenPointsRequestSchema,
    accept_language: AcceptLanguageDep,
) -> RoutePathSchema:
    result = await handler(
        GetRouteBetweenPointsQuery(
            points=[
                Waypoint(latitude=point.latitude, longitude=point.longitude)
                for point in data.waypoints
            ],
            mode=data.mode,
            language=accept_language.language,
        )
    )
    return RoutePathSchema.model_validate(result, from_attributes=True)
