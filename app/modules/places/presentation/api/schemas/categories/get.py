from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import OffsetPaginationSchema


class PlaceCategorySchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="The unique identifier of the place category.",
    )
    slug: str = Field(
        ...,
        description="A unique slug representing the place category.",
    )
    icon_key: str = Field(
        ...,
        description="The key for the icon associated with the place category.",
    )
    name: str = Field(
        ...,
        description="The localized name of the place category.",
    )


class PlaceCategoriesListResponseSchema(BaseModel):
    categories: list[PlaceCategorySchema] = Field(
        ...,
        description="A list of chat previews that match the specified filters and pagination parameters.",
    )
    pagination: OffsetPaginationSchema = Field(
        ...,
        description="Pagination information for the retrieved list of place categories.",
    )
