from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7

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
from app.modules.reviews.presentation.api.v1.routes.schemas.create import (
    CreateReviewRequestSchema,
    CreateReviewResponseSchema,
)
from app.modules.reviews.presentation.api.v1.routes.schemas.get import (
    GetAllReviewsForEntityResponseSchema,
)
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum

places_reviews_router = APIRouter(
    prefix="/places/{place_id}/reviews",
    tags=["Places Reviews"],
)


@places_reviews_router.get("")
@inject
async def get_reviews_for_place(
    place_id: UUID7,
    uc: FromDishka[GetAllReviewsForEntityUseCase],
) -> GetAllReviewsForEntityResponseSchema:
    result = await uc(
        GetAllReviewsForEntityInputDTO(
            entity_id=place_id, entity_type=ReviewEntityTypeEnum.PLACE
        )
    )
    return GetAllReviewsForEntityResponseSchema.model_validate(
        result, from_attributes=True
    )


@places_reviews_router.post(
    "",
    dependencies=[Depends(security)],
)
@inject
async def create_review_for_place(
    uc: FromDishka[CreateReviewUseCase],
    data: CreateReviewRequestSchema,
    principal: Annotated[Principal, Depends(get_principal)],
) -> CreateReviewResponseSchema:
    result = await uc(
        CreateReviewInputDTO(
            author_id=principal.id.value,
            entity_id=data.entity_id,
            entity_type=ReviewEntityTypeEnum.PLACE,
            text=data.text,
            rating=data.rating,
        )
    )
    return CreateReviewResponseSchema.model_validate(result, from_attributes=True)
