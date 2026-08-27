from datetime import datetime

from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import (
    make_paginated_response_schema,
)
from app.modules.places.presentation.api.schemas.categories.category import (
    PlaceCategorySchema,
)
from app.modules.places.presentation.api.schemas.places.address import (
    AdminPlaceAddressSchema,
)
from app.modules.places.presentation.api.schemas.places.category import (
    PlaceCardCategorySchema,
)
from app.modules.places.presentation.api.schemas.places.examples import (
    SHORT_DESCRIPTION_EXAMPLE,
    TIMEZONE_EXAMPLE,
    TITLE_EXAMPLE,
    UUID_EXAMPLE,
)
from app.modules.places.presentation.api.schemas.places.location import (
    PlaceLocationSchema,
)
from app.modules.places.presentation.api.schemas.places.photo import PlacePhotoSchema
from app.modules.places.presentation.api.schemas.places.rating import PlaceRatingSchema
from app.modules.places.presentation.api.schemas.places.working_day import (
    PlaceWorkingDaySchema,
)
from app.modules.places.shared.enums.place_status import PlaceStatusEnum


class BasePlaceCardSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place",
        examples=[UUID_EXAMPLE],
    )
    timezone: str = Field(
        ...,
        description="Timezone of the place",
        examples=[TIMEZONE_EXAMPLE],
    )
    category: PlaceCategorySchema = Field(
        ...,
        description="Category of the place",
    )
    rating: PlaceRatingSchema = Field(
        ...,
        description="Rating of the place",
    )
    location: PlaceLocationSchema = Field(
        ...,
        description="Location of the place",
    )


class PlaceCardSchema(BasePlaceCardSchema):
    title: str = Field(
        ...,
        description="Title of the place",
        examples=[TITLE_EXAMPLE],
    )
    short_description: str = Field(
        ...,
        description="Short description of the place",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    category: PlaceCardCategorySchema = Field(  # type: ignore[assignment]  # intentionally narrower schema for the card view
        ...,
        description="Category of the place",
    )
    photos: list[PlacePhotoSchema] = Field(
        default_factory=list,
        description="Reduced list of place photos.",
    )
    working_days: list[PlaceWorkingDaySchema] = Field(
        default_factory=list,
        description="List of working days for the place.",
    )


class AdminPlaceCardSchema(BasePlaceCardSchema):
    title: str | None = Field(
        None,
        description="Title of the place if available.",
        examples=[TITLE_EXAMPLE],
    )
    address: AdminPlaceAddressSchema = Field(
        ...,
        description="Address of the place.",
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp of the place.",
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp of the place.",
    )
    status: PlaceStatusEnum = Field(
        ...,
        description="Status of the place.",
    )


PaginatedPlaceCardsResponseSchema = make_paginated_response_schema(
    item_type=PlaceCardSchema,
    description="Response schema for a paginated list of place cards.",
)
PaginatedAdminPlaceCardsResponseSchema = make_paginated_response_schema(
    item_type=AdminPlaceCardSchema,
    description="Response schema for a paginated list of place cards for admin users.",
)
