from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)

from app.core.presentation.api.schemas.accept_language import AcceptLanguageDep
from app.core.presentation.api.schemas.pagination import OffsetPaginationDep
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api.v1.users.deps import get_user_principal
from app.modules.auth.shared.context import Principal
from app.modules.places.application.queries.categories.get_all.handler import (
    GetAllPlaceCategoriesQueryHandler,
)
from app.modules.places.application.queries.categories.get_all.query import (
    GetAllPlaceCategoriesQuery,
)
from app.modules.places.presentation.api.schemas.categories.get import (
    PlaceCategoriesListResponseSchema,
)

user_place_categories_router = APIRouter(
    prefix="/places/categories",
    tags=["Place Categories"],
)


@user_place_categories_router.get(
    "",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_place_categories(
    handler: FromDishka[GetAllPlaceCategoriesQueryHandler],
    principal: Annotated[Principal, Depends(get_user_principal)],
    pagination: OffsetPaginationDep,
    accept_language: AcceptLanguageDep,
) -> PlaceCategoriesListResponseSchema:
    result = await handler(
        GetAllPlaceCategoriesQuery(
            language=accept_language.language,
            limit=pagination.limit,
            offset=pagination.offset,
        )
    )
    return PlaceCategoriesListResponseSchema.model_validate(
        result, from_attributes=True
    )
