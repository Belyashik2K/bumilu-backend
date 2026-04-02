from pydantic import (
    BaseModel,
    Field,
)


class PlacePhotoSchema(BaseModel):
    url: str = Field(
        ...,
        description="The URL of the photo.",
        examples=["https://example.com/photo.jpg"],
    )
    thumbnail_url: str = Field(
        ...,
        description="The URL of the thumbnail version of the photo.",
        examples=["https://example.com/photo_thumbnail.jpg"],
    )
