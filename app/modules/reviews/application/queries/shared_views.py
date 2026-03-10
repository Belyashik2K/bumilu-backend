from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import UUID

from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class ReviewAuthorInfoView:
    id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class ReviewEntityInfoView:
    id: UUID
    type: ReviewEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class ReviewInfoView:
    id: UUID
    entity: ReviewEntityInfoView
    author: ReviewAuthorInfoView
    text: str | None = field(default=None)
    rating: int
    created_at: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class ReviewsPage:
    items: list[ReviewInfoView] = field(default_factory=list)
    total: int
