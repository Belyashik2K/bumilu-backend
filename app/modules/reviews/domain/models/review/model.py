from dataclasses import dataclass
from typing import Self

from app.core.domain.value_objects.id import (
    IdVO,
    PrincipalIdVO,
    ReviewIdVO,
)
from app.modules.reviews.domain.value_objects import (
    ReviewRatingVO,
    ReviewTextVO,
)
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


@dataclass(slots=True, kw_only=True)
class Review:
    id: ReviewIdVO
    author_id: PrincipalIdVO
    entity_type: ReviewEntityTypeEnum
    entity_id: IdVO
    text: ReviewTextVO
    rating: ReviewRatingVO

    @classmethod
    def create(
        cls,
        author_id: PrincipalIdVO,
        entity_type: ReviewEntityTypeEnum,
        entity_id: IdVO,
        text: ReviewTextVO,
        rating: ReviewRatingVO,
    ) -> Self:
        return cls(
            id=ReviewIdVO.new(),
            author_id=author_id,
            entity_type=entity_type,
            entity_id=entity_id,
            text=text,
            rating=rating,
        )

    def update(
        self,
        rating: ReviewRatingVO | None = None,
        text: ReviewTextVO | None = None,
    ) -> None:
        if rating is not None and rating != self.rating:
            self.rating = rating
        if text is not None and text != self.text:
            self.text = text
