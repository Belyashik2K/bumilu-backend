from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7

from app.core.shared.constants import UNSET
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.deps import get_principal
from app.modules.auth.shared.context import Principal
from app.modules.reviews.application.use_cases.create import (
    CreateReviewInputDTO,
    CreateReviewUseCase,
)
from app.modules.reviews.application.use_cases.get_all import (
    GetAllReviewsForEntityInputDTO,
    GetAllReviewsForEntityUseCase,
)
from app.modules.reviews.application.use_cases.update import (
    UpdateReviewInputDTO,
    UpdateReviewUseCase,
)
from app.modules.reviews.presentation.api.schemas.common import (
    ENTITY_ID_PATH,
    ENTITY_TYPE_PATH,
    REVIEW_ID_PATH,
)
from app.modules.reviews.presentation.api.schemas.create import (
    CreateReviewRequestSchema,
    CreateReviewResponseSchema,
)
from app.modules.reviews.presentation.api.schemas.get import (
    GetAllReviewsForEntityResponseSchema,
)
from app.modules.reviews.presentation.api.schemas.update import (
    UpdateReviewRequestSchema,
    UpdateReviewResponseSchema,
)
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum

reviews_router = APIRouter(
    tags=["Reviews"],
)


@reviews_router.get("/reviews/{review_id}", dependencies=[Depends(security)])
@inject
async def get_review_by_id(review_id: UUID7 = REVIEW_ID_PATH):
    raise NotImplementedError


@reviews_router.delete("/reviews/{review_id}", dependencies=[Depends(security)])
@inject
async def delete_review_by_id(
    review_id: UUID7 = REVIEW_ID_PATH,
):
    raise NotImplementedError


@reviews_router.patch("/reviews/{review_id}", dependencies=[Depends(security)])
@inject
async def update_review_by_id(
    uc: FromDishka[UpdateReviewUseCase],
    data: UpdateReviewRequestSchema,
    principal: Annotated[Principal, Depends(get_principal)],
    review_id: UUID7 = REVIEW_ID_PATH,
) -> UpdateReviewResponseSchema:
    data_dump = data.model_dump(exclude_unset=True)

    print(data_dump)

    result = await uc(
        UpdateReviewInputDTO(
            review_id=review_id,
            actor_id=principal.id.value,
            text=data_dump.get("text", UNSET),
            rating=data_dump.get("rating", UNSET),
        )
    )
    return UpdateReviewResponseSchema.model_validate(result, from_attributes=True)


@reviews_router.get("/{entity_type}/{entity_id}/reviews")
@inject
async def get_reviews_for_entity(
    uc: FromDishka[GetAllReviewsForEntityUseCase],
    entity_type: ReviewEntityTypeEnum = ENTITY_TYPE_PATH,
    entity_id: UUID7 = ENTITY_ID_PATH,
) -> GetAllReviewsForEntityResponseSchema:
    result = await uc(
        GetAllReviewsForEntityInputDTO(entity_id=entity_id, entity_type=entity_type)
    )
    return GetAllReviewsForEntityResponseSchema.model_validate(
        result, from_attributes=True
    )


@reviews_router.post(
    "/{entity_type}/{entity_id}/reviews",
    dependencies=[Depends(security)],
)
@inject
async def create_review_for_entity(
    uc: FromDishka[CreateReviewUseCase],
    data: CreateReviewRequestSchema,
    principal: Annotated[Principal, Depends(get_principal)],
    entity_type: ReviewEntityTypeEnum = ENTITY_TYPE_PATH,
    entity_id: UUID7 = ENTITY_ID_PATH,
) -> CreateReviewResponseSchema:
    result = await uc(
        CreateReviewInputDTO(
            author_id=principal.id.value,
            entity_type=entity_type,
            entity_id=entity_id,
            text=data.text,
            rating=data.rating,
        )
    )
    return CreateReviewResponseSchema.model_validate(result, from_attributes=True)
