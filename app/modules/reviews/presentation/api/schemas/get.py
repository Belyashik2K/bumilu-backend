from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.reviews.presentation.api.schemas.common import (
    AUTHOR_ID_EXAMPLE,
    ENTITY_ID_EXAMPLE,
    ENTITY_TYPE_EXAMPLE,
    REVIEW_ID_EXAMPLE,
    ReviewInfoSchema,
)
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum

MY_REVIEW_TEXT_EXAMPLE = (
    "Зашёл в точку на Невском буквально на минутку, чтобы узнать, есть ли свободные столики — "
    "администратор сказал что у них в одежде из Ostin'a ходить нельзя - мол не подхожу по статусу. "
    'Я говорю "Давайте сниму", а он "Нет, Вам это не поможет". '
    "Короче спросили за шмот и унизили. "
    "Я ушёл, а администратор продолжал орать на меня, что я не подхожу по статусу и вообще что я на Питоне пишу, "
    "а не на Го, "
    "и что я не могу позволить себе там одежду. "
    "Я в шоке от такого отношения, я не могу поверить, что в 2026 году такое может происходить. "
    "3 звезды только потому, что на телефоне часть экрана не работает и меньше не поставить."
)
MY_REVIEW_RATING_EXAMPLE = 3

MY_REVIEW_EXAMPLE_DATA = {
    "author_id": AUTHOR_ID_EXAMPLE,
    "review_id": REVIEW_ID_EXAMPLE,
    "text": MY_REVIEW_TEXT_EXAMPLE,
    "rating": MY_REVIEW_RATING_EXAMPLE,
}


class ReviewInfoSchemaWithoutEntity(ReviewInfoSchema):
    entity_id: UUID7 = Field(exclude=True)
    entity_type: ReviewEntityTypeEnum = Field(exclude=True)


class ReviewInfoSchemaWithAuthor(ReviewInfoSchema):
    author_id: UUID7 = Field(exclude=True)


class GetAllReviewsByUserResponseSchema(BaseModel):
    user_id: UUID7 = Field(
        ...,
        description="ID of the user (author) for which reviews are fetched",
        examples=[AUTHOR_ID_EXAMPLE],
    )
    items: list[ReviewInfoSchemaWithAuthor] = Field(
        ..., description="List of reviews left by the user (author) fetched"
    )


class GetAllReviewsForEntityResponseSchema(BaseModel):
    entity_id: UUID7 = Field(
        ...,
        description="ID of the entity for which reviews are fetched",
        examples=[ENTITY_ID_EXAMPLE],
    )
    entity_type: ReviewEntityTypeEnum = Field(
        ...,
        description="Type of the entity for which reviews are fetched",
        examples=[ENTITY_TYPE_EXAMPLE],
    )
    my_review: ReviewInfoSchemaWithoutEntity | None = Field(
        None,
        description="Review left by the current user for the entity, if exists",
        alias="actor_review",
        examples=[MY_REVIEW_EXAMPLE_DATA],
    )
    items: list[ReviewInfoSchemaWithoutEntity] = Field(
        ..., description="List of reviews for the entity fetched"
    )
