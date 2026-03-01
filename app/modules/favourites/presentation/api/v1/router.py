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
from app.modules.auth.presentation.api.v1.deps import get_principal
from app.modules.auth.shared.context import Principal
from app.modules.favourites.application.use_cases.add import (
    AddToFavouritesInputDTO,
    AddToFavouritesUseCase,
)
from app.modules.favourites.application.use_cases.get_all_by_user import (
    GetAllFavouritesByUserInputDTO,
    GetAllFavouritesByUserUseCase,
)
from app.modules.favourites.application.use_cases.remove import (
    RemoveFromFavouritesInputDTO,
    RemoveFromFavouritesUseCase,
)
from app.modules.favourites.presentation.api.schemas.common import (
    ENTITY_ID_PATH,
    ENTITY_TYPE_PATH,
    USER_ID_PATH,
)
from app.modules.favourites.presentation.api.schemas.get import (
    GetAllFavouritesByUserResponseSchema,
)
from app.modules.favourites.shared.enums.favourite_entity import FavouriteEntityPathEnum

favourites_router = APIRouter(
    tags=["Favourites"],
    dependencies=[Depends(security)],
)


@favourites_router.get(
    "/users/me/favourites",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def get_my_favourites(
    uc: FromDishka[GetAllFavouritesByUserUseCase],
    principal: Annotated[Principal, Depends(get_principal)],
) -> GetAllFavouritesByUserResponseSchema:
    result = await uc(
        GetAllFavouritesByUserInputDTO(
            actor_id=principal.id.value,
            user_id=principal.id.value,
        )
    )
    return GetAllFavouritesByUserResponseSchema.model_validate(
        result, from_attributes=True
    )


@favourites_router.get(
    "/users/{user_id}/favourites",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def get_favourites_by_user_id(
    uc: FromDishka[GetAllFavouritesByUserUseCase],
    principal: Annotated[Principal, Depends(get_principal)],
    user_id: UUID7 = USER_ID_PATH,
) -> GetAllFavouritesByUserResponseSchema:
    result = await uc(
        GetAllFavouritesByUserInputDTO(
            actor_id=principal.id.value,
            user_id=user_id,
        )
    )
    return GetAllFavouritesByUserResponseSchema.model_validate(
        result, from_attributes=True
    )


@favourites_router.put(
    "/users/me/favourites/{entity_type}/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def add_to_favourites(
    uc: FromDishka[AddToFavouritesUseCase],
    principal: Annotated[Principal, Depends(get_principal)],
    entity_type: FavouriteEntityPathEnum = ENTITY_TYPE_PATH,
    entity_id: UUID7 = ENTITY_ID_PATH,
) -> None:
    await uc(
        AddToFavouritesInputDTO(
            user_id=principal.id.value,
            entity_type=entity_type.domain_name,
            entity_id=entity_id,
        )
    )


@favourites_router.delete(
    "/users/me/favourites/{entity_type}/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def remove_from_favourites(
    uc: FromDishka[RemoveFromFavouritesUseCase],
    principal: Annotated[Principal, Depends(get_principal)],
    entity_type: FavouriteEntityPathEnum = ENTITY_TYPE_PATH,
    entity_id: UUID7 = ENTITY_ID_PATH,
) -> None:
    await uc(
        RemoveFromFavouritesInputDTO(
            user_id=principal.id.value,
            entity_type=entity_type.domain_name,
            entity_id=entity_id,
        )
    )
