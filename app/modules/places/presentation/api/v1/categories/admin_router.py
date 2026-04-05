from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api.v1.staff.deps import get_staff_principal
from app.modules.auth.shared.context import Principal
from app.modules.places.application.commands.categories.create.command import (
    CreatePlaceCategoryCommand,
)
from app.modules.places.application.commands.categories.create.handler import (
    CreatePlaceCategoryCommandHandler,
)
from app.modules.places.application.commands.categories.shared.dtos import (
    NewPlaceCategoryTranslation,
)
from app.modules.places.presentation.api.schemas.categories.create import (
    CreatePlaceCategoryRequestSchema,
    CreatePlaceCategoryResponseSchema,
)

admin_place_categories_router = APIRouter(
    prefix="/admin/places/categories",
    tags=["Admin Place Categories"],
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
