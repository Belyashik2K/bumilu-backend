from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7
from starlette import status

from app.core.presentation.api.schemas.accept_language import (
    AcceptLanguageDep,
)
from app.core.presentation.api.schemas.bbox import BBoxDep
from app.core.presentation.api.schemas.pagination import OffsetPaginationDep
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.users.deps import get_user_principal
from app.modules.auth.shared.context import Principal
from app.modules.places.application.queries.categories.get_all.handler import (
    GetAllPlaceCategoriesQueryHandler,
)
from app.modules.places.application.queries.categories.get_all.query import (
    GetAllPlaceCategoriesQuery,
)
from app.modules.places.application.queries.places.get.handler import (
    GetPlaceQueryHandler,
)
from app.modules.places.application.queries.places.get.query import GetPlaceQuery
from app.modules.places.application.queries.places.get_all.handler import (
    GetAllPlacesQueryHandler,
)
from app.modules.places.application.queries.places.get_all.query import (
    GetAllPlacesQuery,
)
from app.modules.places.application.queries.places.get_map_poi.handler import (
    GetPlacesMapPOIQueryHandler,
)
from app.modules.places.application.queries.places.get_map_poi.query import (
    BBox,
    GetPlacesMapPOIQuery,
)
from app.modules.places.presentation.api.schemas.categories.get import (
    PlaceCategoriesListResponseSchema,
)
from app.modules.places.presentation.api.schemas.places.main import (
    GetPlaceMapPOIsResponseSchema,
    PaginatedPlaceCardsResponseSchema,
    PlaceMapPOISchema,
    PlaceSchema,
)

places_router = APIRouter(
    prefix="/places", tags=["Places"], dependencies=[Depends(security)]
)


@places_router.get(
    "",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_places(
    handler: FromDishka[GetAllPlacesQueryHandler],
    principal: Annotated[Principal, Depends(get_user_principal)],
    pagination: OffsetPaginationDep,
    accept_language: AcceptLanguageDep,
    title_like: str | None = None,
    category_id: UUID7 | None = None,
) -> PaginatedPlaceCardsResponseSchema:
    result = await handler(
        GetAllPlacesQuery(
            title_like=title_like,
            category_id=category_id,
            language=accept_language.language,
            limit=pagination.limit,
            offset=pagination.offset,
        )
    )
    return PaginatedPlaceCardsResponseSchema.model_validate(
        result, from_attributes=True
    )


@places_router.get(
    "/categories",
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


@places_router.get(
    "/map/pois",
    responses=generate_responses_for_endpoint(),
)
@inject
async def get_place_map_pois(
    handler: FromDishka[GetPlacesMapPOIQueryHandler],
    principal: Annotated[Principal, Depends(get_user_principal)],
    accept_language: AcceptLanguageDep,
    bbox: BBoxDep,
) -> GetPlaceMapPOIsResponseSchema:
    result = await handler(
        GetPlacesMapPOIQuery(
            bounds=BBox(
                south=bbox.south,
                west=bbox.west,
                north=bbox.north,
                east=bbox.east,
            ),
            language=accept_language.language,
        )
    )
    return GetPlaceMapPOIsResponseSchema(
        pois=[
            PlaceMapPOISchema.model_validate(poi, from_attributes=True)
            for poi in result
        ]
    )


@places_router.get(
    "/{place_id}",
    responses=generate_responses_for_endpoint(status.HTTP_404_NOT_FOUND),
)
@inject
async def get_place_by_id(
    place_id: UUID7,
    handler: FromDishka[GetPlaceQueryHandler],
    principal: Annotated[Principal, Depends(get_user_principal)],
    accept_language: AcceptLanguageDep,
) -> PlaceSchema:
    result = await handler(
        GetPlaceQuery(
            place_id=place_id,
            language=accept_language.language,
        )
    )
    return PlaceSchema.model_validate(result, from_attributes=True)
