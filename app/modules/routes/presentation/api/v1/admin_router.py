from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7
from starlette import status

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.staff.deps import get_staff_principal
from app.modules.auth.shared.context import Principal
from app.modules.routes.application.commands.create.command import CreateRouteCommand
from app.modules.routes.application.commands.create.handler import (
    CreateRouteCommandHandler,
)
from app.modules.routes.application.commands.delete.command import DeleteRouteCommand
from app.modules.routes.application.commands.delete.handler import (
    DeleteRouteCommandHandler,
)

admin_routes_router = APIRouter(
    prefix="/admin/routes", tags=["Admin Routes"], dependencies=[Depends(security)]
)


@admin_routes_router.post(
    "",
    responses=generate_responses_for_endpoint(),
)
@inject
async def create_route(
    handler: FromDishka[CreateRouteCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(command=CreateRouteCommand())


@admin_routes_router.delete(
    "/{route_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(),
)
@inject
async def delete_route(
    route_id: UUID7,
    handler: FromDishka[DeleteRouteCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(command=DeleteRouteCommand(route_id=route_id))
