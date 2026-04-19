from typing import (
    Annotated,
)

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7
from starlette import status

from app.core.application.queries.pagination import (
    DataListView,
    PaginatedView,
)
from app.core.constants import UNSET
from app.core.enums import LanguageEnum
from app.core.presentation.api.schemas.accept_language import (
    AcceptLanguageDep,
)
from app.core.presentation.api.schemas.pagination import OffsetPaginationDep
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.staff.deps import get_staff_principal
from app.modules.auth.shared.context import Principal
from app.modules.routes.application.commands.change_status.command import (
    ChangeRouteStatusCommand,
)
from app.modules.routes.application.commands.change_status.handler import (
    ChangeRouteStatusCommandHandler,
)
from app.modules.routes.application.commands.create.command import CreateRouteCommand
from app.modules.routes.application.commands.create.handler import (
    CreateRouteCommandHandler,
)
from app.modules.routes.application.commands.create_translation.command import (
    CreateRouteTranslationCommand,
)
from app.modules.routes.application.commands.create_translation.handler import (
    CreateRouteTranslationCommandHandler,
)
from app.modules.routes.application.commands.delete.command import DeleteRouteCommand
from app.modules.routes.application.commands.delete.handler import (
    DeleteRouteCommandHandler,
)
from app.modules.routes.application.commands.delete_translation.command import (
    DeleteRouteTranslationCommand,
)
from app.modules.routes.application.commands.delete_translation.handler import (
    DeleteRouteTranslationCommandHandler,
)
from app.modules.routes.application.commands.replace_points.command import (
    ReplaceRoutePointsCommand,
)
from app.modules.routes.application.commands.replace_points.handler import (
    ReplaceRoutePointsCommandHandler,
)
from app.modules.routes.application.commands.update_translation.command import (
    UpdateRouteTranslationCommand,
)
from app.modules.routes.application.commands.update_translation.handler import (
    UpdateRouteTranslationCommandHandler,
)
from app.modules.routes.application.queries.admin.get_all.handler import (
    GetAdminRoutesListQueryHandler,
)
from app.modules.routes.application.queries.admin.get_all.query import (
    GetAdminRoutesListQuery,
)
from app.modules.routes.application.queries.admin.get_points.handler import (
    GetAdminRoutePointsQueryHandler,
)
from app.modules.routes.application.queries.admin.get_points.query import (
    GetAdminRoutePointsQuery,
)
from app.modules.routes.application.queries.admin.get_translation_by_language_code.handler import (
    GetAdminRouteTranslationByLanguageCodeQueryHandler,
)
from app.modules.routes.application.queries.admin.get_translation_by_language_code.query import (
    GetAdminRouteTranslationByLanguageCodeQuery,
)
from app.modules.routes.application.queries.admin.get_translations.handler import (
    GetAdminRouteTranslationsQueryHandler,
)
from app.modules.routes.application.queries.admin.get_translations.query import (
    GetAdminRouteTranslationsQuery,
)
from app.modules.routes.application.queries.shared.models.route_card import (
    AdminRouteCardReadModel,
)
from app.modules.routes.application.queries.shared.models.route_point import (
    AdminRoutePointReadModel,
)
from app.modules.routes.application.queries.shared.models.route_translation import (
    RouteTranslationReadModel,
)
from app.modules.routes.presentation.api.schemas.main import (
    ChangeRouteStatusRequestSchema,
    CreateRouteResponseSchema,
)
from app.modules.routes.presentation.api.schemas.point import (
    ReplaceRoutePointsRequestSchema,
)
from app.modules.routes.presentation.api.schemas.translation import (
    CreateRouteTranslationRequestSchema,
    UpdateRouteTranslationRequestSchema,
)

admin_routes_router = APIRouter(
    prefix="/admin/routes", tags=["Admin Routes"], dependencies=[Depends(security)]
)


@admin_routes_router.get(
    "",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_routes(
    handler: FromDishka[GetAdminRoutesListQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    accept_language: AcceptLanguageDep,
    pagination: OffsetPaginationDep,
) -> PaginatedView[AdminRouteCardReadModel]:
    result = await handler(
        query=GetAdminRoutesListQuery(
            language=accept_language.language,
            limit=pagination.limit,
            offset=pagination.offset,
        ),
    )
    return result


@admin_routes_router.post(
    "",
    responses=generate_responses_for_endpoint(),
)
@inject
async def create_route(
    handler: FromDishka[CreateRouteCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> CreateRouteResponseSchema:
    result = await handler(command=CreateRouteCommand())
    return CreateRouteResponseSchema.model_validate(result, from_attributes=True)


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


@admin_routes_router.patch(
    "/{route_id}/status",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(),
)
@inject
async def update_route_status(
    route_id: UUID7,
    handler: FromDishka[ChangeRouteStatusCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: ChangeRouteStatusRequestSchema,
) -> None:
    await handler(
        command=ChangeRouteStatusCommand(route_id=route_id, status=data.status)
    )


@admin_routes_router.get(
    "/{route_id}/translations",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_route_translations(
    route_id: UUID7,
    handler: FromDishka[GetAdminRouteTranslationsQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> PaginatedView[RouteTranslationReadModel]:
    result = await handler(
        query=GetAdminRouteTranslationsQuery(
            route_id=route_id,
        )
    )
    return result


@admin_routes_router.post(
    "/{route_id}/translations",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(),
)
@inject
async def create_route_translation(
    route_id: UUID7,
    handler: FromDishka[CreateRouteTranslationCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: CreateRouteTranslationRequestSchema,
) -> None:
    await handler(
        command=CreateRouteTranslationCommand(
            route_id=route_id,
            language_code=data.language_code,
            title=data.title,
            short_description=data.short_description,
            description=data.description,
        )
    )


@admin_routes_router.get(
    "/{route_id}/translations/{language_code}",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_route_translation_by_language_code(
    route_id: UUID7,
    language_code: LanguageEnum,
    handler: FromDishka[GetAdminRouteTranslationByLanguageCodeQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> RouteTranslationReadModel:
    result = await handler(
        query=GetAdminRouteTranslationByLanguageCodeQuery(
            route_id=route_id, language_code=language_code
        )
    )
    return result


@admin_routes_router.patch(
    "/{route_id}/translations/{language_code}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(),
)
@inject
async def update_route_translation(
    route_id: UUID7,
    language_code: LanguageEnum,
    handler: FromDishka[UpdateRouteTranslationCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: UpdateRouteTranslationRequestSchema,
) -> None:
    data_dump = data.model_dump(exclude_unset=True)
    await handler(
        command=UpdateRouteTranslationCommand(
            route_id=route_id,
            language_code=language_code,
            title=data_dump.get("title", UNSET),
            short_description=data_dump.get("short_description", UNSET),
            description=data_dump.get("description", UNSET),
        )
    )


@admin_routes_router.delete(
    "/{route_id}/translations/{language_code}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(),
)
@inject
async def delete_route_translation(
    route_id: UUID7,
    language_code: LanguageEnum,
    handler: FromDishka[DeleteRouteTranslationCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(
        command=DeleteRouteTranslationCommand(
            route_id=route_id,
            language_code=language_code,
        )
    )


@admin_routes_router.get(
    "/{route_id}/points",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_route_points(
    route_id: UUID7,
    handler: FromDishka[GetAdminRoutePointsQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    accept_language: AcceptLanguageDep,
) -> DataListView[AdminRoutePointReadModel]:
    result = await handler(
        query=GetAdminRoutePointsQuery(
            route_id=route_id, language=accept_language.language
        )
    )
    return result


@admin_routes_router.put(
    "/{route_id}/points",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(),
)
@inject
async def replace_route_points(
    route_id: UUID7,
    handler: FromDishka[ReplaceRoutePointsCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: ReplaceRoutePointsRequestSchema,
) -> None:
    await handler(
        command=ReplaceRoutePointsCommand(
            route_id=route_id,
            place_ids=data.place_ids,
        )
    )
