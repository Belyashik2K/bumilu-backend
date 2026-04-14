from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import make_data_list_response_schema
from app.modules.places.presentation.api.schemas.categories.category import (
    PlaceCategorySchema,
)
from app.modules.places.presentation.api.schemas.places.category import (
    PlaceMapPOICategorySchema,
)
from app.modules.places.presentation.api.schemas.places.examples import (
    TITLE_EXAMPLE,
    UUID_EXAMPLE,
)
from app.modules.places.presentation.api.schemas.places.location import (
    PlaceLocationSchema,
)


class BasePlaceMapPOISchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place",
        examples=[UUID_EXAMPLE],
    )
    location: PlaceLocationSchema = Field(
        ...,
        description="Location of the place",
    )


class PlaceMapPOISchema(BasePlaceMapPOISchema):
    title: str = Field(
        ...,
        description="Title of the place",
        examples=[TITLE_EXAMPLE],
    )
    category: PlaceMapPOICategorySchema = Field(
        ...,
        description="Category of the place",
    )


class AdminPlaceMapPOISchema(BasePlaceMapPOISchema):
    title: str | None = Field(
        None,
        description="Title of the place if available.",
        examples=[TITLE_EXAMPLE],
    )
    category: PlaceCategorySchema = Field(
        ...,
        description="Category of the place.",
    )


PlaceMapPOIListResponseSchema = make_data_list_response_schema(
    item_type=PlaceMapPOISchema,
    description="Response schema for a list of places formatted as POIs for map display",
)
AdminPlaceMapPOIListResponseSchema = make_data_list_response_schema(
    item_type=AdminPlaceMapPOISchema,
    description="Response schema for a list of places formatted as POIs for map display for admin users",
)
