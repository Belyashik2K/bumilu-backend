from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.examples import (
    PHOTO_THUMBNAIL_URL_EXAMPLE,
    PHOTO_URL_EXAMPLE,
    UUID_EXAMPLE,
)


class PlacePhotoSchema(BaseModel):
    url: str = Field(
        ...,
        description="The URL of the photo.",
        examples=[PHOTO_URL_EXAMPLE],
    )
    thumbnail_url: str | None = Field(
        None,
        description="The URL of the thumbnail version of the photo.",
        examples=[PHOTO_THUMBNAIL_URL_EXAMPLE],
    )


class StartPlacePhotoUploadRequestSchema(BaseModel):
    content_type: str = Field(
        ..., description="The MIME type of the photo.", examples=["image/jpeg"]
    )


class StartPlacePhotoUploadResponseSchema(BaseModel):
    photo_id: UUID7 = Field(
        ...,
        description="The unique identifier of the photo.",
        examples=[UUID_EXAMPLE],
    )
    file_key: str = Field(
        ...,
        description="The key under which the photo will be stored in the file storage.",
        examples=[
            "places/123e4567-e89b-12d3-a456-426614174000/photos/123e4567-e89b-12d3-a456-426614174001/original.jpg"
        ],
    )
    upload_url: str = Field(
        ...,
        description="The URL to which the photo should be uploaded.",
        examples=[PHOTO_URL_EXAMPLE],
    )
    expires_in: int = Field(
        ...,
        description="The number of seconds until the upload URL expires.",
        examples=[3600],
    )
