from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.examples import (
    PHOTO_THUMBNAIL_URL_EXAMPLE,
    PHOTO_URL_EXAMPLE,
)


class PlacePhotoSchema(BaseModel):
    url: str = Field(
        ...,
        description="The URL of the photo.",
        examples=[PHOTO_URL_EXAMPLE],
    )
    thumbnail_url: str = Field(
        ...,
        description="The URL of the thumbnail version of the photo.",
        examples=[PHOTO_THUMBNAIL_URL_EXAMPLE],
    )
