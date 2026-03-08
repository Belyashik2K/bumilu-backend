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
from app.core.shared.constants import UNSET
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.deps import get_principal
from app.modules.auth.shared.context import Principal
from app.modules.reviews.application.commands.create import (
    CreateReviewCommand,
    CreateReviewCommandHandler,
)
from app.modules.reviews.application.commands.delete import (
    DeleteReviewCommand,
    DeleteReviewCommandHandler,
)
from app.modules.reviews.application.commands.update import (
    UpdateReviewCommand,
    UpdateReviewCommandHandler,
)
from app.modules.reviews.application.queries.get import (
    GetReviewInputDTO,
    GetReviewUseCase,
)
from app.modules.reviews.application.queries.get_all_by_user import (
    GetAllReviewsByUserInputDTO,
    GetAllReviewsByUserUseCase,
)
from app.modules.reviews.application.queries.get_all_for_entity import (
    GetAllReviewsForEntityInputDTO,
    GetAllReviewsForEntityUseCase,
)
from app.modules.reviews.presentation.api.schemas.common import (
    ENTITY_ID_PATH,
    ENTITY_TYPE_PATH,
    REVIEW_ID_PATH,
    USER_ID_PATH,
    ReviewInfoSchema,
)
from app.modules.reviews.presentation.api.schemas.create import (
    CreateReviewRequestSchema,
    CreateReviewResponseSchema,
)
from app.modules.reviews.presentation.api.schemas.get import (
    GetAllReviewsByUserResponseSchema,
    GetAllReviewsForEntityResponseSchema,
)
from app.modules.reviews.presentation.api.schemas.update import (
    UpdateReviewRequestSchema,
    UpdateReviewResponseSchema,
)
from app.modules.reviews.shared.enums import (
    ReviewEntityPathEnum,
)

reviews_router = APIRouter(
    tags=["Reviews"],
    dependencies=[Depends(security)],
)


@reviews_router.get(
    "/users/me/reviews",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def get_my_reviews(
    uc: FromDishka[GetAllReviewsByUserUseCase],
    principal: Annotated[Principal, Depends(get_principal)],
) -> GetAllReviewsByUserResponseSchema:
    result = await uc(
        GetAllReviewsByUserInputDTO(
            user_id=principal.id.value,
            actor_id=principal.id.value,
        )
    )
    return GetAllReviewsByUserResponseSchema.model_validate(
        result, from_attributes=True
    )


@reviews_router.get(
    "/users/{user_id}/reviews",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def get_reviews_by_user_id(
    uc: FromDishka[GetAllReviewsByUserUseCase],
    principal: Annotated[Principal, Depends(get_principal)],
    user_id: UUID7 = USER_ID_PATH,
) -> GetAllReviewsByUserResponseSchema:
    result = await uc(
        GetAllReviewsByUserInputDTO(
            user_id=user_id,
            actor_id=principal.id.value,
        )
    )
    return GetAllReviewsByUserResponseSchema.model_validate(
        result, from_attributes=True
    )


@reviews_router.get(
    "/reviews/{review_id}",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def get_review_by_id(
    uc: FromDishka[GetReviewUseCase],
    principal: Annotated[Principal, Depends(get_principal)],
    review_id: UUID7 = REVIEW_ID_PATH,
) -> ReviewInfoSchema:
    result = await uc(
        GetReviewInputDTO(
            review_id=review_id,
        )
    )
    return ReviewInfoSchema.model_validate(result, from_attributes=True)


@reviews_router.delete(
    "/reviews/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def delete_review_by_id(
    handler: FromDishka[DeleteReviewCommandHandler],
    principal: Annotated[Principal, Depends(get_principal)],
    review_id: UUID7 = REVIEW_ID_PATH,
) -> None:
    await handler(
        DeleteReviewCommand(
            review_id=review_id,
            actor_id=principal.id.value,
        )
    )


@reviews_router.patch(
    "/reviews/{review_id}",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def update_review_by_id(
    handler: FromDishka[UpdateReviewCommandHandler],
    data: UpdateReviewRequestSchema,
    principal: Annotated[Principal, Depends(get_principal)],
    review_id: UUID7 = REVIEW_ID_PATH,
) -> UpdateReviewResponseSchema:
    data_dump = data.model_dump(exclude_unset=True)
    result = await handler(
        UpdateReviewCommand(
            review_id=review_id,
            actor_id=principal.id.value,
            text=data_dump.get("text", UNSET),
            rating=data_dump.get("rating", UNSET),
        )
    )
    return UpdateReviewResponseSchema.model_validate(result, from_attributes=True)


@reviews_router.get(
    "/{entity_type}/{entity_id}/reviews",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def get_reviews_for_entity(
    uc: FromDishka[GetAllReviewsForEntityUseCase],
    principal: Annotated[Principal, Depends(get_principal)],
    entity_type: ReviewEntityPathEnum = ENTITY_TYPE_PATH,
    entity_id: UUID7 = ENTITY_ID_PATH,
) -> GetAllReviewsForEntityResponseSchema:
    result = await uc(
        GetAllReviewsForEntityInputDTO(
            actor_id=principal.id.value,
            entity_id=entity_id,
            entity_type=entity_type.domain_name,
        )
    )
    return GetAllReviewsForEntityResponseSchema.model_validate(
        result, from_attributes=True
    )


@reviews_router.post(
    "/{entity_type}/{entity_id}/reviews",
    status_code=status.HTTP_201_CREATED,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND, status.HTTP_409_CONFLICT
    ),
)
@inject
async def create_review_for_entity(
    handler: FromDishka[CreateReviewCommandHandler],
    data: CreateReviewRequestSchema,
    principal: Annotated[Principal, Depends(get_principal)],
    entity_type: ReviewEntityPathEnum = ENTITY_TYPE_PATH,
    entity_id: UUID7 = ENTITY_ID_PATH,
) -> CreateReviewResponseSchema:
    result = await handler(
        CreateReviewCommand(
            author_id=principal.id.value,
            entity_type=entity_type.domain_name,
            entity_id=entity_id,
            text=data.text,
            rating=data.rating,
        )
    )
    return CreateReviewResponseSchema.model_validate(result, from_attributes=True)
