from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import UUID7

from app.modules.reviews.application.use_cases.get_all import (
    GetAllReviewsForEntityInputDTO,
    GetAllReviewsForEntityUseCase,
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
