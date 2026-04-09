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

from app.core.enums import LanguageEnum
from app.core.presentation.api.schemas.pagination import OffsetPaginationDep
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.staff.deps import get_staff_principal
from app.modules.auth.shared.context import Principal
from app.modules.places.application.commands.categories.create.command import (
    CreatePlaceCategoryCommand,
)
from app.modules.places.application.commands.categories.create.handler import (
    CreatePlaceCategoryCommandHandler,
)
from app.modules.places.application.commands.categories.create_translation.command import (
    CreatePlaceCategoryTranslationCommand,
)
from app.modules.places.application.commands.categories.create_translation.handler import (
    CreatePlaceCategoryTranslationCommandHandler,
)
from app.modules.places.application.commands.categories.delete.command import (
    DeletePlaceCategoryCommand,
)
from app.modules.places.application.commands.categories.delete.handler import (
    DeletePlaceCategoryCommandHandler,
)
from app.modules.places.application.commands.categories.delete_translation.command import (
    DeletePlaceCategoryTranslationCommand,
)
from app.modules.places.application.commands.categories.delete_translation.handler import (
    DeletePlaceCategoryTranslationCommandHandler,
)
from app.modules.places.application.commands.categories.shared.dtos import (
    NewPlaceCategoryTranslation,
)
from app.modules.places.application.commands.categories.update.command import (
    UpdatePlaceCategoryCommand,
)
from app.modules.places.application.commands.categories.update.handler import (
    UpdatePlaceCategoryCommandHandler,
)
from app.modules.places.application.commands.categories.update_translation.command import (
    UpdatePlaceCategoryTranslationCommand,
)
from app.modules.places.application.commands.categories.update_translation.handler import (
    UpdatePlaceCategoryTranslationCommandHandler,
)
from app.modules.places.application.queries.categories.admin.get.handler import (
    GetAdminPlaceCategoryQueryHandler,
)
from app.modules.places.application.queries.categories.admin.get.query import (
    GetAdminPlaceCategoryQuery,
)
from app.modules.places.application.queries.categories.admin.get_all.handler import (
    GetAdminPlaceCategoriesListQueryHandler,
)
from app.modules.places.application.queries.categories.admin.get_all.query import (
    GetAdminPlaceCategoriesListQuery,
)
from app.modules.places.application.queries.categories.admin.get_all_translations.handler import (
    GetAdminPlaceCategoryTranslationsListQueryHandler,
)
from app.modules.places.application.queries.categories.admin.get_all_translations.query import (
    GetAdminPlaceCategoryTranslationsListQuery,
)
from app.modules.places.application.queries.categories.admin.get_translation.handler import (
    GetAdminPlaceCategoryTranslationQueryHandler,
)
from app.modules.places.application.queries.categories.admin.get_translation.query import (
    GetAdminPlaceCategoryTranslationQuery,
)
from app.modules.places.presentation.api.schemas.categories.category import (
    AdminPlaceCategoriesListResponseSchema,
    CreatePlaceCategoryRequestSchema,
    CreatePlaceCategoryResponseSchema,
    PlaceCategorySchema,
    UpdatePlaceCategoryRequestSchema,
)
from app.modules.places.presentation.api.schemas.categories.translation import (
    PaginatedAdminPlaceCategoryTranslationsResponseSchema,
    PlaceCategoryTranslationSchema,
    UpdatePlaceCategoryTranslationRequestSchema,
)

admin_place_categories_router = APIRouter(
    prefix="/admin/places/categories",
    tags=["Admin Place Categories"],
    dependencies=[Depends(security)],
)


@admin_place_categories_router.get(
    "",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_place_categories(
    handler: FromDishka[GetAdminPlaceCategoriesListQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    pagination: OffsetPaginationDep,
) -> AdminPlaceCategoriesListResponseSchema:
    result = await handler(
        GetAdminPlaceCategoriesListQuery(
            actor_id=principal.id.value,
            limit=pagination.limit,
            offset=pagination.offset,
        )
    )
    return AdminPlaceCategoriesListResponseSchema.model_validate(
        result, from_attributes=True
    )


@admin_place_categories_router.post("", responses=generate_responses_for_endpoint())
@inject
async def create_place_category(
    handler: FromDishka[CreatePlaceCategoryCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: CreatePlaceCategoryRequestSchema,
) -> CreatePlaceCategoryResponseSchema:
    result = await handler(
        CreatePlaceCategoryCommand(
            slug=data.slug,
            icon_key=data.icon_key,
            marker_color=data.marker_color,
            translations=[
                NewPlaceCategoryTranslation(
                    language_code=translation.language_code,
                    name=translation.name,
                )
                for translation in data.translations
            ],
        )
    )
    return CreatePlaceCategoryResponseSchema.model_validate(
        result, from_attributes=True
    )


@admin_place_categories_router.get(
    "/{category_id}",
    responses=generate_responses_for_endpoint(status.HTTP_404_NOT_FOUND),
)
@inject
async def get_place_category(
    category_id: UUID7,
    handler: FromDishka[GetAdminPlaceCategoryQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> PlaceCategorySchema:
    result = await handler(
        GetAdminPlaceCategoryQuery(
            category_id=category_id,
            actor_id=principal.id.value,
        )
    )
    return PlaceCategorySchema.model_validate(result, from_attributes=True)


@admin_place_categories_router.patch(
    "/{category_id}",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND, status.HTTP_409_CONFLICT
    ),
)
@inject
async def update_place_category(
    category_id: UUID7,
    handler: FromDishka[UpdatePlaceCategoryCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: UpdatePlaceCategoryRequestSchema,
) -> None:
    await handler(
        UpdatePlaceCategoryCommand(
            category_id=category_id,
            slug=data.slug,
            icon_key=data.icon_key,
            marker_color=data.marker_color,
        )
    )


@admin_place_categories_router.delete(
    "/{category_id}",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND, status.HTTP_409_CONFLICT
    ),
)
@inject
async def delete_place_category(
    category_id: UUID7,
    handler: FromDishka[DeletePlaceCategoryCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(
        DeletePlaceCategoryCommand(
            category_id=category_id,
        )
    )


@admin_place_categories_router.get(
    "/{category_id}/translations",
    responses=generate_responses_for_endpoint(status.HTTP_404_NOT_FOUND),
)
@inject
async def get_place_category_translations(
    category_id: UUID7,
    handler: FromDishka[GetAdminPlaceCategoryTranslationsListQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    pagination: OffsetPaginationDep,
) -> PaginatedAdminPlaceCategoryTranslationsResponseSchema:
    result = await handler(
        GetAdminPlaceCategoryTranslationsListQuery(
            category_id=category_id,
            actor_id=principal.id.value,
            limit=pagination.limit,
            offset=pagination.offset,
        )
    )
    return PaginatedAdminPlaceCategoryTranslationsResponseSchema.model_validate(
        result, from_attributes=True
    )


@admin_place_categories_router.post(
    "/{category_id}/translations",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND, status.HTTP_409_CONFLICT
    ),
)
@inject
async def add_place_category_translation(
    category_id: UUID7,
    handler: FromDishka[CreatePlaceCategoryTranslationCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: PlaceCategoryTranslationSchema,
) -> None:
    await handler(
        CreatePlaceCategoryTranslationCommand(
            category_id=category_id,
            language_code=data.language_code,
            name=data.name,
        )
    )


@admin_place_categories_router.get(
    "/{category_id}/translations/{language_code}",
    responses=generate_responses_for_endpoint(status.HTTP_404_NOT_FOUND),
)
@inject
async def get_place_category_translation(
    category_id: UUID7,
    language_code: LanguageEnum,
    handler: FromDishka[GetAdminPlaceCategoryTranslationQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> PlaceCategoryTranslationSchema:
    result = await handler(
        GetAdminPlaceCategoryTranslationQuery(
            category_id=category_id,
            language_code=language_code,
            actor_id=principal.id.value,
        )
    )
    return PlaceCategoryTranslationSchema.model_validate(result, from_attributes=True)


@admin_place_categories_router.patch(
    "/{category_id}/translations/{language_code}",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND, status.HTTP_409_CONFLICT
    ),
)
@inject
async def update_place_category_translation(
    category_id: UUID7,
    language_code: LanguageEnum,
    handler: FromDishka[UpdatePlaceCategoryTranslationCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: UpdatePlaceCategoryTranslationRequestSchema,
) -> None:
    await handler(
        UpdatePlaceCategoryTranslationCommand(
            category_id=category_id,
            language_code=language_code,
            name=data.name,
        )
    )


@admin_place_categories_router.delete(
    "/{category_id}/translations/{language_code}",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def delete_place_category_translation(
    category_id: UUID7,
    language_code: LanguageEnum,
    handler: FromDishka[DeletePlaceCategoryTranslationCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(
        DeletePlaceCategoryTranslationCommand(
            category_id=category_id,
            language_code=language_code,
        )
    )
