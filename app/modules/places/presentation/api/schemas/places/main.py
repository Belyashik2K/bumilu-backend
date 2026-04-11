from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import OffsetPaginationSchema
from app.modules.places.presentation.api.schemas.categories.examples import SLUG_EXAMPLE
from app.modules.places.presentation.api.schemas.places.address import (
    PlaceAddressSchema,
)
from app.modules.places.presentation.api.schemas.places.category import (
    PlaceCardCategorySchema,
    PlaceMapPOICategorySchema,
)
from app.modules.places.presentation.api.schemas.places.examples import (
    DESCRIPTION_EXAMPLE,
    SHORT_DESCRIPTION_EXAMPLE,
    TAXI_ADDRESS_EXAMPLE,
    TAXI_COMMENT_EXAMPLE,
    TIMEZONE_EXAMPLE,
    TITLE_EXAMPLE,
    UUID_EXAMPLE,
)
from app.modules.places.presentation.api.schemas.places.location import (
    PlaceLocationSchema,
)
from app.modules.places.presentation.api.schemas.places.phone import PlacePhoneSchema
from app.modules.places.presentation.api.schemas.places.photo import PlacePhotoSchema
from app.modules.places.presentation.api.schemas.places.rating import PlaceRatingSchema
from app.modules.places.presentation.api.schemas.places.user_context import (
    PlaceUserContextSchema,
)
from app.modules.places.presentation.api.schemas.places.working_day import (
    PlaceWorkingDaySchema,
)


class PlaceMapPOISchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place",
        examples=[UUID_EXAMPLE],
    )
    title: str = Field(
        ...,
        description="Title of the place",
        examples=[TITLE_EXAMPLE],
    )
    category: PlaceMapPOICategorySchema = Field(
        ...,
        description="Category of the place",
    )
    location: PlaceLocationSchema = Field(
        ...,
        description="Location of the place",
    )


class GetPlaceMapPOIsResponseSchema(BaseModel):
    pois: list[PlaceMapPOISchema] = Field(
        default_factory=list,
        description="A list of places formatted as POIs for map display.",
    )


class PlaceCardSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place",
        examples=[UUID_EXAMPLE],
    )
    title: str = Field(
        ...,
        description="Title of the place",
        examples=[TITLE_EXAMPLE],
    )
    short_description: str | None = Field(
        None,
        description="Short description of the place",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    timezone: str = Field(
        ...,
        description="Timezone of the place",
        examples=[TIMEZONE_EXAMPLE],
    )
    category: PlaceCardCategorySchema = Field(
        ...,
        description="Category of the place",
    )
    photos: list[PlacePhotoSchema] = Field(
        default_factory=list,
        description="List of place photos. Maximum of 4 photos are allowed for the place card.",
    )
    rating: PlaceRatingSchema = Field(
        ...,
        description="Rating of the place",
    )
    location: PlaceLocationSchema = Field(
        ...,
        description="Location of the place",
    )
    working_days: list[PlaceWorkingDaySchema] = Field(
        default_factory=list,
        description="List of working days for the place.",
    )


class PaginatedPlaceCardsResponseSchema(BaseModel):
    places: list[PlaceCardSchema] = Field(
        default_factory=list,
        description="A list of place cards",
    )
    pagination: OffsetPaginationSchema = Field(
        ...,
        description="Pagination information for the retrieved places.",
    )


class PlaceSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place",
        examples=[UUID_EXAMPLE],
    )
    title: str = Field(
        ...,
        description="Title of the place",
        examples=[TITLE_EXAMPLE],
    )
    description: str | None = Field(
        None,
        description="Description of the place",
        examples=[DESCRIPTION_EXAMPLE],
    )
    short_description: str | None = Field(
        None,
        description="Short description of the place",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    timezone: str = Field(
        ...,
        description="Timezone of the place",
        examples=[TIMEZONE_EXAMPLE],
    )
    category: PlaceCardCategorySchema = Field(
        ...,
        description="Category of the place",
    )
    photos: list[PlacePhotoSchema] = Field(
        default_factory=list,
        description="List of place photos",
    )
    address: PlaceAddressSchema = Field(
        ...,
        description="Address of the place",
    )
    rating: PlaceRatingSchema = Field(
        ...,
        description="Rating of the place",
    )
    location: PlaceLocationSchema = Field(
        ...,
        description="Location of the place",
    )
    phones: list[PlacePhoneSchema] = Field(
        default_factory=list,
        description="List of place phones",
    )
    working_days: list[PlaceWorkingDaySchema] = Field(
        default_factory=list,
        description="List of working days for the place.",
    )
    user_context: PlaceUserContextSchema = Field(
        ...,
        description="User-specific context for the place, such as whether it's in the user's favorites.",
    )


class CreatePlaceRequestSchema(BaseModel):
    category_slug: str = Field(
        ...,
        description="Slug of the place category",
        examples=[SLUG_EXAMPLE],
    )
    location: PlaceLocationSchema = Field(
        ...,
        description="Location of the place",
    )
    address_taxi: str = Field(
        ...,
        description="Taxi address of the place",
        examples=[TAXI_ADDRESS_EXAMPLE],
    )
    address_taxi_comment: str | None = Field(
        None,
        description="Optional comment for the taxi address",
        examples=[TAXI_COMMENT_EXAMPLE],
    )


class CreatePlaceResponseSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the created place",
        examples=[UUID_EXAMPLE],
    )


class UpdatePlaceRequestSchema(BaseModel):
    category_slug: str | None = Field(
        None,
        description="Slug of the place category",
        examples=[SLUG_EXAMPLE],
    )
    location: PlaceLocationSchema | None = Field(
        None,
        description="Location of the place",
    )
    address_taxi: str | None = Field(
        None,
        description="Taxi address of the place",
        examples=[TAXI_ADDRESS_EXAMPLE],
    )
    address_taxi_comment: str | None = Field(
        None,
        description="Optional comment for the taxi address",
        examples=[TAXI_COMMENT_EXAMPLE],
    )
